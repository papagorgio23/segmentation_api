import streamlit as st


from functions import (
    load_models,
    plot_preds,
    prediction_result,
    user_data_prep,
    user_input_features,
)


st.set_page_config(
    page_title="Model Demo",
    page_icon="🚀",
)

LOGO = "./img/actblue.png"

# Title
st.title("Contribution Model")

# Subheader
st.subheader("_Adjust the inputs in the sidebar to get predictions_")
st.write("***")


# Logo
st.sidebar.image(LOGO, use_column_width=True)
st.sidebar.text("Jason Lee\nSr. Data Scientist")
st.sidebar.write("***")
st.sidebar.markdown("### User Inputs")


# Sidebar User Inputs
input_df = user_input_features()
st.sidebar.write("***")


# load models
model = load_models()

# Prediction
user_prepped = user_data_prep(input_df)
prediction = prediction_result(model, user_prepped)
st.subheader("Prediction:")

# print the prediction in dollars
pred = prediction["Predicted Donation"].values[0]
st.subheader(f"${pred:.2f}")


fig = plot_preds(prediction)
st.plotly_chart(fig)


# Footer
# add a few blank lines in markdown
st.markdown("---")
st.sidebar.write("\n\n\n\n\n\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("\n")
st.sidebar.write("***")
st.sidebar.text("© 2024 ActBlue")
st.sidebar.text("All rights reserved.")
st.sidebar.text("Version 0.1")
st.sidebar.text("Built with Streamlit")
