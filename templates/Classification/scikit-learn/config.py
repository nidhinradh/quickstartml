import streamlit as st

models = ["SVM", "Stochastic Gradient Descent", "Logistic Regression", "Random Forest Classifier", "K-Neighbors Classifier"]
performance_evaluation_methods = ["Accuracy Score", "Confusion Matrix"]

def show():
    configs = {}

    with st.sidebar:
        st.subheader("Pre-processing")
        configs["is_normalization"] =  st.checkbox("Normalization", value=False)
        configs["train_test_method"] = st.radio("Splitting Data", ("Seperate Test Dataset", "Train-Test Split"))
        configs["split_percentage"] = 0.2
        if(configs["train_test_method"] == "Train-Test Split"):
            configs["split_percentage"] = st.slider("Test Size", 0.01, 0.99, 0.2)

        st.subheader("Model")
        configs["selected_model"] = st.selectbox("Select Model", sorted(models))

        if(configs["selected_model"] == "SVM" or configs["selected_model"] == "Stochastic Gradient Descent" or configs["selected_model"] == "Random Forest Classifier"):
            configs["random_state"] = st.number_input('Random State', value=0, step=1)
        
        if(configs["selected_model"] == "K-Neighbors Classifier"):
            configs["n_neighbors"] = st.number_input('Neighbors', value=5, step=1)
        
        st.subheader("Post Processing")
        configs["performance_evaluation_methods"] = st.selectbox("Select Performance Evaluation Method", sorted(performance_evaluation_methods))
        
    return configs

if __name__ == "__main__":
    show()