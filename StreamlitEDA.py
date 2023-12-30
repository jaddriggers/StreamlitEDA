import datetime
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile
import io

# Title and intro
st.title("Upload CSV (or CSV inside ZIP) for EDA and Statistics")
st.write(
    "This application is a Streamlit dashboard that can be used to upload a CSV (or CSV inside ZIP) for EDA and Statistics")

# CSV Upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Check if it's a zip file
    if zipfile.is_zipfile(uploaded_file):
        with zipfile.ZipFile(uploaded_file) as z:
            with z.open(z.namelist()[0]) as f:
                df = pd.read_csv(f)
    else:
        df = pd.read_csv(uploaded_file)

    # Show dataframe
    st.write(df)
    st.write(df.dtypes)

    # column ot change data types
    col_to_change = st.sidebar.selectbox("Select column to change data type: ", df.columns)
    new_type = st.sidebar.selectbox("Select new data type: ", ['float', 'int', 'string', 'datetime'])
    if st.sidebar.button("Change Data Type"):
        if new_type == 'float':
            df[col_to_change] = df[col_to_change].astype(float)
        elif new_type == 'int':
            df[col_to_change] = df[col_to_change].astype(int)
        elif new_type == 'string':
            df[col_to_change] = df[col_to_change].astype(str)
        elif new_type == 'datetime':
            df[col_to_change] = df[col_to_change].astype(datetime)

    # Show statistics
    st.write(df.describe())
    st.write(df.info())
    st.write(df.dtypes)

    # Select numerical columns to plot
    numerical_columns = df.select_dtypes(include=['float64', 'int']).columns.tolist()
    if not numerical_columns:
        st.write("No numerical columns found in the dataset.")
    else:
        st.subheader("Visualize Data")
        columns_to_plot = st.multiselect("Select the numerical columns to plot", numerical_columns)

    if len(columns_to_plot) > 0:
        fig = sns.pairplot(data=df[columns_to_plot])
        plt.show()
        st.pyplot()
