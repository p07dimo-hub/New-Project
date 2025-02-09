import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


st.set_page_config(page_title="Data Mining App", layout="wide")
st.title("Web-Based Data Mining and Analysis App")


menu = ["Home", "Upload Data", "Visualization", "Feature Selection", "Classification", "Results", "Info"]
choice = st.sidebar.selectbox("Navigation", menu)


def load_data():
    uploaded_file = st.file_uploader("Upload CSV, Excel, or TSV file", type=["csv", "xlsx", "tsv"])
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1]
        if ext == "csv":
            df = pd.read_csv(uploaded_file)
        elif ext == "tsv":
            df = pd.read_csv(uploaded_file, sep="\t")
        else:
            df = pd.read_excel(uploaded_file)
        return df
    return None

data = None
if choice in ["Visualization", "Feature Selection", "Classification", "Results"]:
    data = load_data()
    if data is not None:
        st.write("### Preview of the Dataset")
        st.dataframe(data.head())

if choice == "Visualization":
    if data is not None:
        target_column = st.selectbox("Select Label Column", data.columns)
        feature_columns = [col for col in data.columns if col != target_column]
        
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(data[feature_columns])
        df_pca = pd.DataFrame(pca_data, columns=["PC1", "PC2"])
        df_pca[target_column] = data[target_column]
        fig_pca = px.scatter(df_pca, x="PC1", y="PC2", color=target_column, title="PCA 2D Visualization")
        st.plotly_chart(fig_pca)
        
        umap = UMAP(n_components=2)
        umap_data = umap.fit_transform(data[feature_columns])
        df_umap = pd.DataFrame(umap_data, columns=["UMAP1", "UMAP2"])
        df_umap[target_column] = data[target_column]
        fig_umap = px.scatter(df_umap, x="UMAP1", y="UMAP2", color=target_column, title="UMAP 2D Visualization")
        st.plotly_chart(fig_umap)

if choice == "Feature Selection":
    if data is not None:
        target_column = st.selectbox("Select Label Column", data.columns)
        num_features = st.slider("Select Number of Features", min_value=1, max_value=len(data.columns)-1, value=5)
        feature_columns = [col for col in data.columns if col != target_column]
        
        selector = SelectKBest(score_func=f_classif, k=num_features)
        X_new = selector.fit_transform(data[feature_columns], data[target_column])
        selected_features = [feature_columns[i] for i in selector.get_support(indices=True)]
        st.write("### Selected Features")
        st.write(selected_features)
        st.dataframe(data[selected_features + [target_column]].head())

if choice == "Classification":
    if data is not None:
        target_column = st.selectbox("Select Label Column", data.columns)
        feature_columns = [col for col in data.columns if col != target_column]
        X_train, X_test, y_train, y_test = train_test_split(data[feature_columns], data[target_column], test_size=0.2, random_state=42)
        
        model_choice = st.selectbox("Choose Classifier", ["K-Nearest Neighbors", "Random Forest"])
        if model_choice == "K-Nearest Neighbors":
            k = st.slider("Choose k", min_value=1, max_value=20, value=5)
            model = KNeighborsClassifier(n_neighbors=k)
        else:
            trees = st.slider("Choose number of trees", min_value=10, max_value=100, value=50)
            model = RandomForestClassifier(n_estimators=trees)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        roc_auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr')
        
        st.write(f"### Accuracy: {accuracy:.2f}")
        st.write(f"### F1 Score: {f1:.2f}")
        st.write(f"### ROC AUC: {roc_auc:.2f}")

if choice == "Info":
    st.write("### Application Information")
    st.write("Descreption:This application was developed to assist with data mining and analysis.")
    st.write("Developer Team:Apostolos Dimos")
    st.write("Apostolos Dimos: Data processing and visualization")
    st.write("Apostolos Dimos: Selection of characteristics and categorization")
    st.write("Apostolos Dimos: Development and integration with Docker")
    st.write("Apostolos Dimos: Reference documentation and tests")