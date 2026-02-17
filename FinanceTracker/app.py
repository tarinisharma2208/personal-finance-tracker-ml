import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.title("Personal Finance Tracker (Beginner Version)")

# Upload CSV
uploaded_file = st.file_uploader("Upload Your Bank Statement (CSV)", type=["csv"])
sample_csv_path = Path(__file__).resolve().parent / "sample.csv"

if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif sample_csv_path.exists():
    st.info(f"No CSV uploaded. Using sample file: {sample_csv_path}")
    df = pd.read_csv(sample_csv_path)
else:
    st.info("Please upload a CSV file to begin.")
    st.stop()

# Check required columns
required_cols = ["date", "description", "amount", "category"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    st.error("CSV must contain: date, description, amount, category")
    st.write("Missing columns:", missing)
    # Offer sample CSV for download
    try:
        sample_text = sample_csv_path.read_text(encoding="utf-8") if sample_csv_path.exists() else "date,description,amount,category\n"
    except Exception:
        sample_text = "date,description,amount,category\n"
    st.download_button("Download sample CSV", data=sample_text, file_name="sample.csv", mime="text/csv")
else:
    st.subheader("Your Transactions")
    st.write(df)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    # Filter expenses (negative amounts)
    expense_df = df[df["amount"] < 0]

    # Total expense
    total_expense = expense_df["amount"].sum()
    st.subheader("Total Expense")
    st.write(f"INR {abs(total_expense)}")

    # Category-wise expense
    category_summary = expense_df.groupby("category")["amount"].sum().abs()
    st.subheader("Category-wise Expense")
    st.bar_chart(category_summary)

    # Pie Chart
    st.subheader("Expense Distribution")
    fig, ax = plt.subplots()
    ax.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%")
    st.pyplot(fig)

    # Monthly Expense
    monthly_summary = expense_df.groupby("month")["amount"].sum().abs()
    st.subheader("Monthly Expense")
    st.line_chart(monthly_summary)
