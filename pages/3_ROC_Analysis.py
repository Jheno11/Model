import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

st.title("Gene ROC Analysis")

st.header("Input Files")
upregulated_file = st.file_uploader("Upload UpRegulated Dataset", type=['csv', 'xlsx'])
combined_dataset_file = st.file_uploader("Upload Combined Dataset", type=['csv', 'xlsx'])

# ROC Curve AUC Threshold
auc_threshold = st.slider("AUC Threshold", min_value=0.5, max_value=1.0, value=0.9, step=0.05)

if upregulated_file and combined_dataset_file:
    # Load data
    data = pd.read_csv(upregulated_file)
    geneID = data.iloc[:,0]
    features_df = data.iloc[:,1:]
    data = data.set_index("Ensembl_ID")
    data = data.T
    data['label'] = ['cancer' if '-01' in sample else 'normal' for sample in data.index]
    
    # Sample count information
    st.header("Sample Information")
    class_counts = data['label'].value_counts()
    st.write(f"Total cancer samples: {class_counts['cancer']}")
    st.write(f"Total normal samples: {class_counts['normal']}")
    st.write(f"Total samples: {len(data)}")
    
    # Prepare data for ROC
    X = np.asarray(features_df.round().astype(int).T)
    y = np.asarray(data['label'])
    
    y_bin = label_binarize(y, classes=np.unique(y))
    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(X.shape[1]):
        fpr[i], tpr[i], _ = roc_curve(y_bin.ravel(), X[:, i].ravel())
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Create ROC DataFrame
    roc_df = pd.DataFrame({
        'Ensembl_ID': geneID,
        'ROC': [roc_auc[i] for i in range(len(geneID))]
    })
    
    # Plot ROC Curve
    st.header("ROC Curve")
    plt.figure(figsize=(10, 8))
    
    high_auc_genes = []
    for i in range(len(geneID)):
        if roc_auc[i] > auc_threshold:
            plt.plot(fpr[i], tpr[i], lw=2, label=f'Gene {geneID[i]} (AUC = {roc_auc[i]:.4f})')
            high_auc_genes.append(geneID[i])
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for Genes with AUC > {auc_threshold}')
    plt.legend(loc="lower right")
    st.pyplot(plt)
    
    # Display high AUC genes
    st.header("High AUC Genes")
    st.write(f"Genes with AUC > {auc_threshold}:")
    st.write(high_auc_genes)
    
    # Filter Combined Dataset
    st.header("Filtered Dataset")
    combined_dataset = pd.read_csv(combined_dataset_file)
    regulated_genes = combined_dataset[combined_dataset['Ensembl_ID'].isin(high_auc_genes)]
    st.dataframe(regulated_genes)

    # Download option
    @st.cache_data
    def convert_to_excel(df, file_path):
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='ROC_Results')
        return file_path

    # Save DataFrame to a temporary path
    file_path = convert_to_excel(regulated_genes, "ROC_Results.xlsx")

    st.download_button(
        label="Download ROC_Results as XLSX",
        data=open(file_path, "rb").read(),
        file_name="ROC_Results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )