import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import zipfile


def read_file(uploaded_file):
    if zipfile.is_zipfile(uploaded_file):
        with zipfile.ZipFile(uploaded_file) as z:
            with z.open(z.namelist()[0]) as f:
                return pd.read_csv(f)
    else:
        return pd.read_csv(uploaded_file)


def change_dtypes(df, col_to_change, new_type):
    if new_type == 'datetime':
        new_type = 'datetime64[ns]'
    df[col_to_change] = df[col_to_change].astype(new_type)


def visualize_data(df):
    numerical_columns = df.select_dtypes(include=['float64', 'int']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    if not numerical_columns and not categorical_columns:
        st.write("No numerical or categorical columns found in the dataset.")
    else:

        st.subheader("Visualize Data")
        column_type = st.selectbox("Choose the type of columns to visualize", ["Numerical", "Categorical"])

        if column_type == "Numerical":
            if numerical_columns:
                columns_to_plot = st.multiselect("Select the numerical columns to plot", numerical_columns)
                if columns_to_plot:
                    fig = sns.pairplot(data=df[columns_to_plot])
                    st.pyplot(fig)
            else:
                st.write("No numerical columns available for plotting")

        else:  # Categorical
            if categorical_columns:
                columns_to_plot = st.multiselect("Select the categorical columns to plot", categorical_columns)
                if columns_to_plot:
                    for column in columns_to_plot:
                        fig, ax = plt.subplots()
                        sns.countplot(x=column, data=df)
                        st.pyplot(fig)
            else:
                st.write("No categorical columns available for plotting")


st.title("Upload CSV (or CSV inside ZIP) for EDA and Statistics")
st.write(
    "This application is a Streamlit dashboard that can be used to upload a CSV (or CSV inside ZIP) for EDA and Statistics")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = read_file(uploaded_file)
    st.write("Display the first 5 rows of the dataframe:")
    st.write(df.head(5))

    col_to_change = st.sidebar.selectbox("Select column to change data type: ", df.columns)
    new_type = st.sidebar.selectbox("Select new data type: ", ['float', 'int', 'string', 'datetime'])
    if st.sidebar.button("Change Data Type"):
        change_dtypes(df, col_to_change, new_type)

    st.write("Display summary statistics of the dataframe:")
    st.write(df.describe())

    visualize_data(df)


