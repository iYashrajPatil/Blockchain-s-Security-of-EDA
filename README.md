# 🔍 Blockchain-Secured Regional Sales Analysis

## 📌 Final Year Major Project

This project enhances traditional sales analytics by integrating **Blockchain technology** to ensure **data integrity, authenticity, and tamper detection**.  
It combines **EDA, Ethereum smart contracts, Streamlit, and Power BI** to build a trust-aware analytics system.

---

## 🧠 Problem Statement

Sales analytics pipelines often involve multiple systems, making datasets vulnerable to:
- Unauthorized modification
- Accidental data corruption
- Lack of trust in analytical insights

This project ensures that the **data used for analysis is verifiable and tamper-proof** using blockchain.

---

## 🚀 Solution Overview

- Perform EDA on regional sales data
- Generate deterministic SHA-256 hash of cleaned dataset
- Store hash on Ethereum Sepolia testnet via smart contract
- Verify dataset integrity through a Streamlit interface
- Visualize insights using Power BI dashboards

---

## 🏗️ Project Structure

Blockchain-Secured-EDA/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│ ├── EDA_Regional_Sales_Analysis.ipynb
│ └── Blockchain_Part.ipynb
│
├── data/
│ ├── Regional_Sales_Dataset.xlsx
│ └── Sales_data_Cleaned.csv
│
├── assets/
│ └── logo.png
│
├── presentation/
│ └── Regional_Sales_Analysis.pptx


---

## 🛠️ Tech Stack

- **Python** (Pandas, NumPy, Matplotlib, Seaborn)
- **Blockchain** (Ethereum, SHA-256, Web3.py)
- **Frontend**: Streamlit
- **BI Tool**: Power BI
- **Smart Contracts**: Solidity (Remix IDE)

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
Note: secrets.env is required for blockchain interaction and is not included in the repository.
```

## 📈 Key Results

✔ 100% accuracy in detecting tampered datasets

✔ Identified seasonal and regional sales trends

✔ Enabled non-technical users to verify data integrity

✔ Improved trust in analytics-driven decisions

## 🔮 Future Scope

Ethereum mainnet deployment

Real-time sales data pipelines

Predictive analytics and anomaly detection

Extension to healthcare and supply chain domains

## 👨‍🎓 Author

Yashraj Patil
Final Year Engineering Student
Aspiring Data Scientist