import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import zipfile

# EXTRACT CONSTANT for datetime dtype
DATETIME_TYPE = 'datetime64[ns]'


def read_file(uploaded_file):
    if zipfile.is_zipfile(uploaded_file):
        with zipfile.ZipFile(uploaded_file) as z:
            with z.open(z.namelist()[0]) as f:
                return pd.read_csv(f)
    else:
        return pd.read_csv(uploaded_file)


def change_dtypes(df, col_to_change, new_type):
    if new_type == 'datetime':
        new_type = DATETIME_TYPE
    df[col_to_change] = df[col_to_change].astype(new_type)


# EXTRACT FUNCTION for plotting
def plot_columns(df, columns_to_plot, column_type):
    if columns_to_plot:
        if column_type == "Numerical":
            fig = sns.pairplot(data=df[columns_to_plot])
            st.pyplot(fig)
        else:  # Categorical
            for column in columns_to_plot:
                fig, ax = plt.subplots()
                sns.countplot(x=column, data=df)
                st.pyplot(fig)
    else:
        st.write(f"No {column_type.lower()} columns available for plotting")


def visualize_data(df):
    numerical_columns = df.select_dtypes(include=['float64', 'int']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    if not numerical_columns and not categorical_columns:
        st.write("No numerical or categorical columns found in the dataset.")
    else:
        st.subheader("Visualize Data")
        column_type = st.selectbox("Choose the type of columns to visualize", ["Numerical", "Categorical"])
        columns_to_select = numerical_columns if column_type == "Numerical" else categorical_columns
        columns_to_plot = st.multiselect(f"Select the {column_type.lower()} columns to plot", columns_to_select)
        plot_columns(df, columns_to_plot, column_type)


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
