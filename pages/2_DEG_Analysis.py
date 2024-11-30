import streamlit as st
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import numpy as np

# Advanced Styling
st.set_page_config(page_title="Gene Expression Analysis", layout="wide")

# App Title
st.title("Differential Gene Expression Analysis with PyDESeq2")

# File Uploads
st.header("Input Files")
racial_dataset = st.file_uploader("Upload Data (.csv OR .xlsx)", type=["csv", "xlsx"])

if racial_dataset:
    st.write("Processing dataset....")
    if racial_dataset.name.endswith(".csv"):
        data = pd.read_csv(racial_dataset)
    elif racial_dataset.name.endswith(".xlsx"):
        data = pd.read_excel(racial_dataset, engine="openpyxl")
        data = pd.read_excel(racial_dataset, engine="openpyxl")
    data = data.set_index("Ensembl_ID")
    data = data.fillna(0)
    data = data.round().astype(np.int32)
    data = data[data.sum(axis=1) > 0]
    data = data.T

    st.write("Preprocessed Counts Data")
    st.dataframe(data.head(5))

    # Create Metadata
    def create_metadata(counts_data):
        conditions = ['cancer' if '-01' in sample else 'normal' for sample in counts_data.index]
        metadata = pd.DataFrame({'Ensembl_ID': counts_data.index, 'Condition': conditions})
        metadata = metadata.set_index('Ensembl_ID')
        return metadata

    metadata = create_metadata(data)
    st.write("Metadata")
    st.dataframe(metadata)

    def initiate_deg(counts_data, metadata):
        dds = DeseqDataSet(
            counts=counts_data,
            metadata=metadata,
            design_factors="Condition",
            n_cpus=-1
        )
        dds.deseq2()
        stat_res = DeseqStats(dds, contrast=("Condition", "cancer", "normal"))
        stat_res.summary()
        return stat_res.results_df

    deg_stats_results = initiate_deg(data, metadata)
    st.write("DEG Statistics Results", deg_stats_results)

    # Filter DEG Results
    st.header("DEG Filtering Options")
    cutoff_padj = st.number_input("Cutoff for padj", value=0.05)
    cutoff_log2FoldChange = st.number_input("Cutoff for log2FoldChange", value=0.0)
    cutoff_baseMean = st.number_input("Cutoff for baseMean", value=10)

    def filter_deg_results(deg_results):
        deg_results = deg_results[deg_results['padj'] < cutoff_padj]
        deg_results = deg_results[deg_results['log2FoldChange'].abs() > cutoff_log2FoldChange]
        deg_results = deg_results[deg_results['baseMean'] >= cutoff_baseMean]
        return deg_results

    filtered_deg_results = filter_deg_results(deg_stats_results)
    st.write("Filtered DEG Results", filtered_deg_results)

    # Display DEG Genes
    st.write("DEG Genes", filtered_deg_results.index.to_list())