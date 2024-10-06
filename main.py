import pandas as pd
import streamlit as st
import preprocessor

# Main script
df = pd.read_csv('Big_Black_Money_Dataset.csv')

# Adding an Image
image_url = "Black Money Transactions Analysis.png"
st.sidebar.image(image_url)

# Sidebar Filters
selected_country, selected_transaction_types, amount_range = preprocessor.sidebar_filters(df)

# Apply Filters
filtered_df = preprocessor.apply_filters(df, selected_country, selected_transaction_types, amount_range)

# Display Dashboard Sections
st.title("Black Money Transactions Analysis")

# Total Transactions
preprocessor.display_total_transactions(filtered_df)

# Total Amount by Industry
preprocessor.display_total_amount_by_industry(filtered_df)

# Transaction Amount Distribution
preprocessor.display_transaction_amount_distribution(filtered_df)

# Money Laundering Risk Score Analysis
preprocessor.display_risk_score_analysis(filtered_df)

# Pie Chart of Transaction Types
preprocessor.display_transaction_type_distribution(filtered_df)

# Scatter Plot: Amount vs. Risk Score
preprocessor.display_scatter_plot(filtered_df)

# Summary Statistics
preprocessor.display_summary_statistics(filtered_df)
