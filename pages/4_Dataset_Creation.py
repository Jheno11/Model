import streamlit as st
import pandas as pd

st.title("Dataset Creation")
st.write("Module to Create Dataset for Machine Learning Modelling")


# File Uploaders
st.header("Upload Input Files")
deg_file = st.file_uploader("Upload DEG Genes File", type=['csv'])
dataset_file = st.file_uploader("Upload Combined Dataset", type=['csv'])

if deg_file and dataset_file:
    # Read Files
    ensembl_id = pd.read_csv(deg_file)
    dataset = pd.read_csv(dataset_file)

    # Get Ensembl IDs
    ensembl_ids = ensembl_id['Ensembl_ID']
    
    # Display First Few Ensembl IDs
    st.header("First Few Ensembl IDs")
    st.dataframe(ensembl_ids.head())

    # Filter Dataset
    regulated_genes = dataset[dataset['Ensembl_ID'].isin(ensembl_ids)]
    regulated_genes = regulated_genes.set_index('Ensembl_ID')

    # Display Filtered Genes
    st.header("Regulated Genes")
    st.dataframe(regulated_genes)

    # Save Option
    st.download_button(
        label="Download Filtered Genes",
        data=regulated_genes.to_csv(index=True),
        file_name='regulated_genes.csv',
        mime='text/csv'
    )