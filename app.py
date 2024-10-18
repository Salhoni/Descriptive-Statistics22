import streamlit as st
import pandas as pd

# Set the page configuration for a dark theme
st.set_page_config(page_title="Descriptive Statistics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark theme and bold font
st.markdown(
    """
    <style>
    body {
        background-color: #181818; /* Dark background */
        color: #ffffff; /* White text */
        font-weight: bold; /* Bold font */
    }
    .stTextInput, .stFileUploader, .stSelectbox {
        background-color: #303030; /* Darker input boxes */
        color: #ffffff; /* White text */
        border: 1px solid #ffffff; /* White border */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File upload section
st.title("Descriptive Statistics App")
st.write("Upload your CSV, Excel, or TXT file to get descriptive statistics.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    # Detect file type and load data accordingly
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        df = pd.read_csv(uploaded_file, delimiter='\t')

    # Display the dataset
    st.write("### Dataset Preview")
    st.write(df.head())

    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Additional options for advanced analysis can be added here

# Display footer information
st.write("---")
st.write("Made with ❤️ using Streamlit.")
