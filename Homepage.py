import streamlit as st

st.set_page_config(page_title="Homepage", page_icon=":penguin:", layout="wide", initial_sidebar_state="expanded")

st.title("Optimized Feature Selection for Cancer Detection")
st.write("Please make sure the sample IDs is using the TCGA format!")

st.write("1. The Data Segragation page contain file for phenotype file and counts file that will be spearate and match based on the white race")

st.write("2. DEG analysis page used dataset that have been merged from previous page, in this page there are several step to conduct DEG : ")
st.write("- Cleaning data by dropping missing value and rounding the value to integer")
st.write("- Labelling the data with normal and cancer so DEG can be computed")
st.write("- Use feature selection to select best gene, the best gene will be used for ROC analysis")

st.write("3. Use ROC analysis to find best gene that will be used for modelling")

st.write("4. Use modelling (SVM, Naive Bayes, Logistic Regression) to find best model that will be used for prediction")
st.write("- The dataset that will be used is from ROC analysis")
st.write("- The first step is splitting the data for normal and cancer")
st.write("- The second step is balancing the data using balancing technique with ratio 1:3")
st.write("- The third step is using hyperparameter tuning to find best model")
st.write("- The hyperparameter for each model is different")
st.write("- The result for each model will be shown in the result table")