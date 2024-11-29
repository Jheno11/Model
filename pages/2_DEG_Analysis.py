import streamlit as st
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# App Title
st.title("Differential Gene Expression Analysis with PyDESeq2")

# File Uploads
st.header("Input Files")
racial_dataset = st.file_uploader("Upload Phenotype Data (.csv OR .xlsx)", type=["csv", "xlsx"])

if racial_dataset:
    st.write("Processing dataset....")
    
    # Efficient file reading
    if racial_dataset.name.endswith(".csv"):
        data = pd.read_csv(racial_dataset, dtype="int32")
    elif racial_dataset.name.endswith(".xlsx"):
        data = pd.read_excel(racial_dataset, dtype="int32")

    # Preprocessing
    data.set_index("Ensembl_ID")
    data.fillna(0, inplace=True)
    data = data.round().astype("int32")
    data = data[data.sum(axis=1) > 0]
    data = data.T

    st.write("Preprocessed Counts Data")
    st.dataframe(data.head(5))

    # Create Metadata using vectorized operations
    conditions = ['cancer' if '-01' in sample else 'normal' for sample in data.index]
    metadata = pd.DataFrame({'Ensembl_ID': data.index, 'Condition': conditions})
    metadata.set_index('Ensembl_ID', inplace=True)
    st.write("Metadata")
    st.dataframe(metadata)

    # DEG Analysis - Only necessary columns
    def initiate_deg(counts_data, metadata):
        dds = DeseqDataSet(
            counts=counts_data,
            metadata=metadata,
            design_factors="Condition"
        )
        dds.deseq2()
        stat_res = DeseqStats(dds, contrast=("label", "cancer", "normal"))
        stat_res.summary()
        return stat_res.results_df[['padj', 'log2FoldChange', 'baseMean', 'pvalue', 'lfcSE', 'stat']]

    deg_stats_results = initiate_deg(data, metadata)
    st.write("DEG Statistics Results", deg_stats_results)

    # Filter DEG Results
    st.header("DEG Filtering Options")
    cutoff_padj = st.number_input("Cutoff for padj", value=0.05)
    cutoff_log2FoldChange = st.number_input("Cutoff for log2FoldChange", value=0.0)
    cutoff_baseMean = st.number_input("Cutoff for baseMean", value=10)
    cutoff_pvalue = st.number_input("Cutoff for pvalue", value=0.0)
    cutoff_lfcSE = st.number_input("Cutoff for lfcSE", value=0.0)
    cutoff_stat = st.number_input("Cutoff for stat", value=0.0)

    def filter_deg_results(deg_results):
        # Use chained condition for filtering in one go
        return deg_results[
            (deg_results['padj'] < cutoff_padj) &
            (deg_results['log2FoldChange'].abs() > cutoff_log2FoldChange) &
            (deg_results['baseMean'] > cutoff_baseMean) &
            (deg_results['pvalue'] < cutoff_pvalue) &
            (deg_results['lfcSE'] > cutoff_lfcSE) &
            (deg_results['stat'].abs() > cutoff_stat)
        ]

    filtered_deg_results = filter_deg_results(deg_stats_results)
    st.write("Filtered DEG Results", filtered_deg_results)

    # Display DEG Genes
    st.write("DEG Genes", filtered_deg_results.index.to_list())
