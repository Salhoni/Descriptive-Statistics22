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
    .stTextInput, .stFileUploader, .stTextArea {
        background-color: #303030; /* Darker input boxes */
        color: #ffffff; /* White text */
        border: 1px solid #ffffff; /* White border */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to calculate descriptive statistics
def calculate_statistics(data):
    return data.describe()

# Title of the app
st.title("Descriptive Statistics App")
st.write("Upload your CSV, Excel, or TXT file or input numerical values to get descriptive statistics.")

# File upload section
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

# Direct input section
st.write("Or enter numerical values (one per line):")
input_values = st.text_area("Input values", height=150)

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

    # Calculate and display summary statistics
    st.write("### Summary Statistics")
    st.write(calculate_statistics(df))

# Process direct input
elif input_values:
    try:
        # Convert input values into a DataFrame
        input_list = [float(i) for i in input_values.splitlines() if i]
        input_df = pd.DataFrame(input_list, columns=["Values"])

        # Calculate and display summary statistics
        st.write("### Summary Statistics for Input Values")
        st.write(calculate_statistics(input_df))

    except ValueError:
        st.error("Please enter valid numerical values, one per line.")

# Display footer information
st.write("---")
st.write("Made with ❤️ using Streamlit.")
