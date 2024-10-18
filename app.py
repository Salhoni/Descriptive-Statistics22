import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
    return {
        "Mean": np.mean(data),
        "Standard Error": stats.sem(data),
        "Median": np.median(data),
        "Mode": stats.mode(data).mode[0],
        "Standard Deviation": np.std(data, ddof=1),  # Sample standard deviation
        "Sample Variance": np.var(data, ddof=1),  # Sample variance
        "Kurtosis": stats.kurtosis(data),
        "Skewness": stats.skew(data),
        "Range": np.ptp(data),  # Peak to peak (max - min)
        "Minimum": np.min(data),
        "Maximum": np.max(data),
        "Sum": np.sum(data),
        "Count": len(data)
    }

# Function to create visualizations
def plot_statistics(statistics):
    fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(15, 10))
    axs = axs.flatten()

    # Create visualizations for each statistic
    metrics = list(statistics.keys())
    values = list(statistics.values())
    
    for i in range(len(metrics)):
        axs[i].bar(metrics[i], values[i], color='skyblue')
        axs[i].set_title(metrics[i])
        axs[i].set_ylabel('Value')
        axs[i].set_ylim(min(values) - 5, max(values) + 5)  # Set y-axis limits for better visualization
    
    plt.tight_layout()
    st.pyplot(fig)

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

    # Perform descriptive statistics
    st.write("### Summary Statistics")
    statistics = calculate_statistics(df.select_dtypes(include=np.number).values.flatten())
    st.write(statistics)

    # Create visualizations
    plot_statistics(statistics)

# Process direct input
elif input_values:
    try:
        # Convert input values into a DataFrame
        input_list = [float(i) for i in input_values.splitlines() if i]
        input_df = pd.DataFrame(input_list, columns=["Values"])

        # Calculate descriptive statistics
        st.write("### Summary Statistics for Input Values")
        statistics = calculate_statistics(input_df["Values"])
        st.write(statistics)

        # Create visualizations
        plot_statistics(statistics)

    except ValueError:
        st.error("Please enter valid numerical values, one per line.")

# Display footer information
st.write("---")
st.write("Made with ❤️ using Streamlit.")
