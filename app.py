import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

# Set the page configuration for a dark theme
st.set_page_config(page_title="Descriptive Statistics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark theme and formal font
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5; /* Light background for better contrast */
        color: #333333; /* Dark text color */
        font-family: Arial, sans-serif; /* Formal font */
    }
    .stTextInput, .stFileUploader, .stTextArea {
        background-color: #ffffff; /* White input boxes */
        color: #333333; /* Dark text */
        border: 1px solid #cccccc; /* Light gray border */
    }
    .table-container {
        border: 1px solid #333333; /* Border around the table */
        padding: 10px;
        border-radius: 5px;
        background-color: #ffffff; /* White background for the table */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to calculate descriptive statistics
def calculate_statistics(data):
    if len(data) == 0:
        return {"Error": "No data provided."}
    
    try:
        mode = stats.mode(data).mode[0] if len(data) > 0 else np.nan
    except Exception:
        mode = np.nan

    return {
        "Mean": np.mean(data),
        "Standard Error": stats.sem(data) if len(data) > 1 else np.nan,
        "Median": np.median(data),
        "Mode": mode,
        "Standard Deviation": np.std(data, ddof=1) if len(data) > 1 else np.nan,  # Sample standard deviation
        "Sample Variance": np.var(data, ddof=1) if len(data) > 1 else np.nan,  # Sample variance
        "Kurtosis": stats.kurtosis(data) if len(data) > 1 else np.nan,
        "Skewness": stats.skew(data) if len(data) > 1 else np.nan,
        "Range": np.ptp(data) if len(data) > 1 else np.nan,  # Peak to peak (max - min)
        "Minimum": np.min(data) if len(data) > 0 else np.nan,
        "Maximum": np.max(data) if len(data) > 0 else np.nan,
        "Sum": np.sum(data),
        "Count": len(data)
    }

# Title of the app
st.title("Descriptive Statistics App")
st.write("Upload your CSV, Excel, or TXT file or input numerical values to get descriptive statistics.")

# File upload section
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

# Direct input section
st.write("Or enter numerical values separated by commas:")
input_values = st.text_input("Input values", placeholder="e.g., 10, 20, 30, 40")

# Process uploaded file
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

    # Perform descriptive statistics
    st.write("### Summary Statistics")
    statistics = calculate_statistics(df.select_dtypes(include=np.number).values.flatten())
    stats_df = pd.DataFrame(statistics.items(), columns=["Statistic", "Value"])
    
    with st.container():
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        st.table(stats_df)
        st.markdown("</div>", unsafe_allow_html=True)

# Process direct input
elif input_values:
    try:
        # Convert input values into a list of floats
        input_list = [float(i.strip()) for i in input_values.split(',') if i.strip()]
        input_df = pd.DataFrame(input_list, columns=["Values"])

        # Calculate descriptive statistics
        st.write("### Summary Statistics for Input Values")
        statistics = calculate_statistics(input_df["Values"])
        stats_df = pd.DataFrame(statistics.items(), columns=["Statistic", "Value"])
        
        with st.container():
            st.markdown("<div class='table-container'>", unsafe_allow_html=True)
            st.table(stats_df)
            st.markdown("</div>", unsafe_allow_html=True)

    except ValueError:
        st.error("Please enter valid numerical values, separated by commas.")

# Display footer information
st.write("---")
st.write("Made with ❤️ using Streamlit.")

