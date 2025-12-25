import streamlit as st
import pandas as pd
import hashlib
import os, json
from web3 import Web3
from dotenv import load_dotenv

# === Load secrets ===
load_dotenv("secrets.env")
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = Web3.to_checksum_address(os.getenv("WALLET_ADDRESS"))
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# === Connect to Sepolia ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# === Load ABI (replace with your contract ABI) ===
abi_json = '''
[
  {
    "inputs": [
      { "internalType": "string", "name": "datasetName", "type": "string" },
      { "internalType": "string", "name": "hashValue", "type": "string" }
    ],
    "name": "storeHash",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "string", "name": "datasetName", "type": "string" }
    ],
    "name": "getHash",
    "outputs": [
      { "internalType": "string", "name": "", "type": "string" }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
'''
abi = json.loads(abi_json)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# === Helper: deterministic hash ===
def deterministic_hash_dataframe(df: pd.DataFrame) -> str:
    df2 = df.copy()
    df2 = df2.reindex(sorted(df2.columns), axis=1)
    df2 = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
    return hashlib.sha256(df2.to_csv(index=False).encode("utf-8")).hexdigest()

# === Helper: anchor hash ===
def anchor_hash(dataset_name: str, hash_value: str):
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
    tx = contract.functions.storeHash(dataset_name, hash_value).build_transaction({
        "from": WALLET_ADDRESS,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    raw_tx = getattr(signed_tx, "rawTransaction", None) or getattr(signed_tx, "raw_transaction", None)
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# === Helper: verify hash ===
def verify_hash(dataset_name: str, local_hash: str) -> (bool, str):
    onchain_hash = contract.functions.getHash(dataset_name).call()
    return onchain_hash == local_hash, onchain_hash

# === Streamlit UI ===
st.set_page_config(page_title="Blockchain Data Integrity", page_icon="🔗", layout="wide")

# Logo + Header
try:
    st.image("logo.png", width=120)
except:
    pass

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🔗 Blockchain Data Integrity Checker</h1>",
    unsafe_allow_html=True
)
st.write("Upload a dataset, anchor its fingerprint on Sepolia, and verify integrity.")

# Sidebar walkthrough
st.sidebar.title("📖 How to Use")
st.sidebar.markdown("""
1. **Upload CSV** → Preview + hash generated  
2. **Anchor on Blockchain** → Store hash on Sepolia  
3. **Verify Integrity** → Compare dataset vs blockchain  
4. **Tamper Demo** → See how even 1 change breaks verification  
5. **Mini‑EDA** → Only runs if dataset is verified ✅
""")

uploaded_file = st.file_uploader("Upload your CSV dataset", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    dataset_hash = deterministic_hash_dataframe(df)
    st.code(f"SHA-256 Hash: {dataset_hash}", language="text")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Anchor on Blockchain"):
            receipt = anchor_hash("sales_data", dataset_hash)
            st.success(f"✅ Anchored successfully! Tx hash: {receipt.transactionHash.hex()}")

    with col2:
        if st.button("🔍 Verify Integrity"):
            verified, onchain_hash = verify_hash("sales_data", dataset_hash)
            if verified:
                st.success("✅ Integrity verified — dataset matches blockchain record")

                # Mini EDA preview
                st.subheader("📈 Mini EDA (Trusted Data Only)")
                st.write(df.describe())
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])  # first 2 numeric cols

            else:
                st.error(f"❌ Mismatch! On-chain hash: {onchain_hash}")

    with col3:
        if st.button("⚠️ Tamper Demo"):
            df_tampered = df.copy()
            first_num_col = next((c for c in df_tampered.columns if pd.api.types.is_numeric_dtype(df_tampered[c])), None)
            if first_num_col:
                df_tampered.loc[0, first_num_col] += 1
            tampered_hash = deterministic_hash_dataframe(df_tampered)
            verified, onchain_hash = verify_hash("sales_data", tampered_hash)
            st.warning("Tampered dataset hash: " + tampered_hash)
            if not verified:
                st.error("❌ Tampered dataset failed verification (as expected)")

# Footer
st.markdown(
    "<hr><p style='text-align: center; color: grey;'>Built by Team Yashraj • Powered by EDA + Blockchain + Streamlit</p>",
    unsafe_allow_html=True
)
