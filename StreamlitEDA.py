import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import zipfile

# EXTRACT CONSTANT for datetime dtype
DATETIME_TYPE = 'datetime64[ns]'

SUMMARY_MESSAGE = "Display summary statistics of the dataframe:"

def read_file(uploaded_file):
    """
    Reads a file and returns its contents as a Pandas DataFrame.

    :param uploaded_file: The file to be read. This can be either a CSV file or a ZIP file containing a single CSV file.
    :return: A Pandas DataFrame containing the contents of the file.
    """
    if zipfile.is_zipfile(uploaded_file):
        with zipfile.ZipFile(uploaded_file) as z:
            with z.open(z.namelist()[0]) as f:
                return pd.read_csv(f)
    else:
        return pd.read_csv(uploaded_file)


def change_dtypes(df, col_to_change, new_type):
    """
    Change the data type of a specific column in a DataFrame.

    :param df: The DataFrame in which the column's data type needs to be changed.
    :type df: pandas.DataFrame
    :param col_to_change: The name of the column to change its data type.
    :type col_to_change: str
    :param new_type: The new data type to be assigned to the column. Supported values: 'datetime', 'int', 'float', 'object', 'bool'.
    :type new_type: str
    :return: The DataFrame with the updated data type for the specified column.
    :rtype: pandas.DataFrame
    """
    if new_type == 'datetime':
        new_type = DATETIME_TYPE
    df[col_to_change] = df[col_to_change].astype(new_type)


# EXTRACT FUNCTION for plotting
def plot_columns(df, columns_to_plot, column_type):
    """
    :param df: DataFrame containing the data to be plotted.
    :param columns_to_plot: List of column names to be plotted.
    :param column_type: Type of the columns to be plotted. Possible values are "Numerical" or "Categorical".
    :return: None

    This method plots the specified columns from the given DataFrame based on their type. If the column type is "Numerical", a pair plot is created using seaborn library and displayed using
    * streamlit library. If the column type is "Categorical", individual count plots are created for each column using seaborn library and displayed using streamlit library. If no columns
    * are available for plotting based on the given column type, a message is displayed using streamlit library.
    """
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
    """
    Visualizes numerical or categorical columns in a given DataFrame.

    :param df: Pandas DataFrame to visualize.
    :return: None.
    """
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
    new_type = st.sidebar.selectbox("Select new data type: ", ['float', 'int', 'string', 'datetime', 'object'])
    if st.sidebar.button("Change Data Type"):
        change_dtypes(df, col_to_change, new_type)

    # st.markdown("---")
    # st.markdown("### Adjust column datatypes:")
    # for col in df.columns:
    #     new_type = st.selectbox(f"Select new data type for {col}: ",
    #                             ['float', 'int', 'string', 'datetime'], key=col)
    #     if st.button("Change Data Type", key=col):
    #         change_dtypes(df, col, new_type)
    # st.markdown("---")
df_description = df.describe(include='object')

st.write(SUMMARY_MESSAGE)
st.write('Numerical stats')
st.dataframe(df.describe())

st.write('Categorical stats')
st.dataframe(df_description)

st.write('Count of null values')
st.dataframe(df.isnull().sum())



st.write("Display data types of each column:")
st.write(df.dtypes)

visualize_data(df)
