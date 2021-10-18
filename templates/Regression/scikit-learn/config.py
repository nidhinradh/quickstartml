import streamlit as st

models = ["Linear Regression", "Decision Tree", "Random Forest Classifier"]
performance_evaluation_methods = ["Mean Absolute Error", "Mean Squared Error", "R2 Score"]

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

        if(configs["selected_model"] == "Decision Tree" or configs["selected_model"] == "Random Forest Classifier"):
            configs["random_state"] = st.number_input('Random State', value=0, step=1)
        
        if(configs["selected_model"] == "Random Forest Classifier"):
            configs["max_depth"] = st.number_input('Max Depth', value=2, step=1)
        
        st.subheader("Post Processing")
        configs["performance_evaluation_methods"] = st.selectbox("Select Performance Evaluation Method", sorted(performance_evaluation_methods))
        
    return configs

if __name__ == "__main__":
    show()