import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Personal Finance Tracker (Beginner Version)")

# Upload CSV
uploaded_file = st.file_uploader("Upload Your Bank Statement (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    required_cols = ["date", "description", "amount", "category"]
    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain: date, description, amount, category")
    else:
        st.subheader("📋 Your Transactions")
        st.write(df)

        # Convert date column
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month

        # Filter expenses (negative amounts)
        expense_df = df[df["amount"] < 0]

        # Total expense
        total_expense = expense_df["amount"].sum()
        st.subheader("💸 Total Expense")
        st.write(f"₹ {abs(total_expense)}")

        # Category-wise expense
        category_summary = expense_df.groupby("category")["amount"].sum().abs()

        st.subheader("📊 Category-wise Expense")
        st.bar_chart(category_summary)

        # Pie Chart
        st.subheader("🥧 Expense Distribution")
        fig, ax = plt.subplots()
        ax.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%')
        st.pyplot(fig)

        # Monthly Expense
        monthly_summary = expense_df.groupby("month")["amount"].sum().abs()

        st.subheader("📅 Monthly Expense")
        st.line_chart(monthly_summary)

else:
    st.info("Please upload a CSV file to begin.")
