import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")



# Read and clean the dataset
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df['Date of Transaction'] = pd.to_datetime(df['Date of Transaction'], errors='coerce')
    df.dropna(inplace=True)
    return df

# Sidebar filter options
def sidebar_filters(df):
    st.sidebar.header("Filter Options")
    
    # Country Filter
    countries = df['Country'].unique().tolist()
    selected_country = st.sidebar.selectbox("Select Country", ['All'] + countries)
    
    # Transaction Type Filter
    transaction_types = df['Transaction Type'].unique().tolist()
    transaction_types = ['All'] + transaction_types
    selected_transaction_types = st.sidebar.multiselect("Select Transaction Types", transaction_types)
    
    # Amount Range Filter
    min_amount = df['Amount (USD)'].min()
    max_amount = df['Amount (USD)'].max()
    amount_range = st.sidebar.slider("Select Amount Range", min_value=float(min_amount), max_value=float(max_amount), value=(min_amount, max_amount))
    
    return selected_country, selected_transaction_types, amount_range

# Apply filters
def apply_filters(df, selected_country, selected_transaction_types, amount_range):
    filtered_df = df.copy()
    
    # Apply country filter
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]

    # Apply transaction type filter
    if 'All' not in selected_transaction_types:
        filtered_df = filtered_df[filtered_df['Transaction Type'].isin(selected_transaction_types)]
    
    # Apply amount range filter
    filtered_df = filtered_df[filtered_df['Amount (USD)'].between(amount_range[0], amount_range[1])]
    
    return filtered_df

# Total Transactions
def display_total_transactions(filtered_df):
    total_transactions = filtered_df['Transaction ID'].count()
    st.subheader(f"Total Transactions: {total_transactions}")

# Total Amount by Industry
def display_total_amount_by_industry(filtered_df):
    if not filtered_df.empty:
        industry_summary = filtered_df.groupby('Industry')['Amount (USD)'].sum().reset_index()
        st.subheader("Total Amount by Industry")

        # Create plot
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=industry_summary, x='Industry', y='Amount (USD)', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.subheader("No data available for the selected filters.")

# Transaction Amount Distribution
def display_transaction_amount_distribution(filtered_df):
    if not filtered_df.empty:
        st.subheader("Transaction Amount Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(filtered_df['Amount (USD)'], bins=50, kde=True, ax=ax)
        ax.set_title('Distribution of Transaction Amounts')
        st.pyplot(fig)



# Money Laundering Risk Score Analysis
def display_risk_score_analysis(filtered_df):
    if not filtered_df.empty:
        st.subheader("Money Laundering Risk Score Analysis")
        risk_summary = filtered_df['Money Laundering Risk Score'].value_counts().reset_index()
        risk_summary.columns = ['Risk Score', 'Count']

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=risk_summary, x='Risk Score', y='Count', ax=ax)
        ax.set_title('Count of Transactions by Money Laundering Risk Score')
        st.pyplot(fig)

# Pie Chart of Transaction Types
def display_transaction_type_distribution(filtered_df):
    if not filtered_df.empty:
        st.subheader("Transaction Types Distribution")
        transaction_type_summary = filtered_df['Transaction Type'].value_counts()

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(transaction_type_summary, labels=transaction_type_summary.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# Scatter Plot: Amount vs. Risk Score
def display_scatter_plot(filtered_df):
    if not filtered_df.empty:
        st.subheader("Scatter Plot: Amount vs. Risk Score")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.scatterplot(data=filtered_df, x='Money Laundering Risk Score', y='Amount (USD)', ax=ax)
        ax.set_title('Scatter Plot of Amount vs. Money Laundering Risk Score')
        st.pyplot(fig)

# Summary Statistics
def display_summary_statistics(filtered_df):
    if not filtered_df.empty:
        st.subheader("Summary Statistics")
        st.write(filtered_df.describe())
    else:
        st.write("No data available for the selected filters.")
