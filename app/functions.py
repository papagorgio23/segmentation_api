import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


### STATIC DATA
features = [
    # "contributor_employer",
    "first_time_donor",
    "earmarked_bernie",
    "earmarked_actblue",
    "earmarked_biden",
    "earmarked_warren",
    "earmarked_pete",
    "earmarked_dccc",
    "earmarked_stop",
    "earmarked_amy",
    "earmarked_dscc",
    "earmarked_ecup",
    "occ_not_emp",
    "occ_teacher",
    "occ_retired",
    "occ_law",
    "occ_eng",
    "occ_prof",
    "occ_swe",
    "occ_dr",
    "occ_sales",
    "occ_consult",
    "occ_manager",
    "occ_nurse",
    "occ_self",
    "state_AB",
    "state_AE",
    "state_AK",
    "state_AL",
    "state_AP",
    "state_AR",
    "state_AS",
    "state_AZ",
    "state_BC",
    "state_CA",
    "state_CO",
    "state_CT",
    "state_DC",
    "state_DE",
    "state_FL",
    "state_GA",
    "state_GU",
    "state_HI",
    "state_IA",
    "state_ID",
    "state_IL",
    "state_IN",
    "state_KS",
    "state_KY",
    "state_LA",
    "state_MA",
    "state_MB",
    "state_MD",
    "state_ME",
    "state_MI",
    "state_MN",
    "state_MO",
    "state_MP",
    "state_MS",
    "state_MT",
    "state_NB",
    "state_NC",
    "state_ND",
    "state_NE",
    "state_NH",
    "state_NJ",
    "state_NL",
    "state_NM",
    "state_NS",
    "state_NV",
    "state_NY",
    "state_OH",
    "state_OK",
    "state_ON",
    "state_OR",
    "state_PA",
    "state_PE",
    "state_PR",
    "state_QC",
    "state_RI",
    "state_SC",
    "state_SD",
    "state_TN",
    "state_TX",
    "state_UT",
    "state_VA",
    "state_VI",
    "state_VT",
    "state_WA",
    "state_WI",
    "state_WV",
    "state_WY",
    "state_YT",
    "state_ZZ",
]

earmark = [
    "ActBlue",
    "Amy for America",
    "Biden",
    "Bernie",
    "DCCC",
    "DSCC",
    "End Citizens United",
    "Pete for America",
    "Stop Republicans",
    "Warren",
    "Other",
]

occupations = [
    "ATTORNEY",
    "CONSULTANT",
    "ENGINEER",
    "LAWYER",
    "MANAGER",
    "NOT EMPLOYED",
    "NURSE",
    "PHYSICIAN",
    "PROFESSOR",
    "RETIRED",
    "RN",
    "SALES",
    "SELF EMPLOYED",
    "SOFTWARE ENGINEER",
    "TEACHER",
    "OTHER",
]


states = [
    "AB",
    "AE",
    "AK",
    "AL",
    "AP",
    "AR",
    "AS",
    "AZ",
    "BC",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "GU",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MB",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MP",
    "MS",
    "MT",
    "NB",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NL",
    "NM",
    "NS",
    "NV",
    "NY",
    "OH",
    "OK",
    "ON",
    "OR",
    "PA",
    "PE",
    "PR",
    "QC",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VI",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
    "YT",
    "ZZ",
]


@st.cache_data()
def load_models():
    # load best saved model
    best_model = joblib.load("./models/contribution_model_2024-04-18.pkl")
    return best_model


def user_input_features():

    first_time = st.sidebar.selectbox("First Time Donation?", ("Yes", "No"), index=0)
    earmark_type = st.sidebar.selectbox("Donation Purpose:", earmark, index=0)
    occupation = st.sidebar.selectbox("Donor Occupation", (occupations))
    us_state = st.sidebar.selectbox("Donor State", (states))

    inputs = {
        "first_time": [first_time],
        "earmark_type": [earmark_type],
        "occupation": [occupation],
        "state": [us_state],
    }

    return inputs


# function to perform all the data cleaning/feature engineering
def user_data_prep(inputs: dict) -> pd.DataFrame:

    # user inputs
    first_time = inputs["first_time"][0]
    earmark_type = inputs["earmark_type"][0]
    occupation = inputs["occupation"][0]
    us_state = inputs["state"][0]

    # dataframe that will be populated with user inputs used for prediction
    final_df = pd.DataFrame(
        np.zeros((1, 93), dtype="int64"),
        columns=[
            "first_time_donor",
            "earmarked_bernie",
            "earmarked_actblue",
            "earmarked_biden",
            "earmarked_warren",
            "earmarked_pete",
            "earmarked_dccc",
            "earmarked_stop",
            "earmarked_amy",
            "earmarked_dscc",
            "earmarked_ecup",
            "occ_not_emp",
            "occ_teacher",
            "occ_retired",
            "occ_law",
            "occ_eng",
            "occ_prof",
            "occ_swe",
            "occ_dr",
            "occ_sales",
            "occ_consult",
            "occ_manager",
            "occ_nurse",
            "occ_self",
            "state_AB",
            "state_AE",
            "state_AK",
            "state_AL",
            "state_AP",
            "state_AR",
            "state_AS",
            "state_AZ",
            "state_BC",
            "state_CA",
            "state_CO",
            "state_CT",
            "state_DC",
            "state_DE",
            "state_FL",
            "state_GA",
            "state_GU",
            "state_HI",
            "state_IA",
            "state_ID",
            "state_IL",
            "state_IN",
            "state_KS",
            "state_KY",
            "state_LA",
            "state_MA",
            "state_MB",
            "state_MD",
            "state_ME",
            "state_MI",
            "state_MN",
            "state_MO",
            "state_MP",
            "state_MS",
            "state_MT",
            "state_NB",
            "state_NC",
            "state_ND",
            "state_NE",
            "state_NH",
            "state_NJ",
            "state_NL",
            "state_NM",
            "state_NS",
            "state_NV",
            "state_NY",
            "state_OH",
            "state_OK",
            "state_ON",
            "state_OR",
            "state_PA",
            "state_PE",
            "state_PR",
            "state_QC",
            "state_RI",
            "state_SC",
            "state_SD",
            "state_TN",
            "state_TX",
            "state_UT",
            "state_VA",
            "state_VI",
            "state_VT",
            "state_WA",
            "state_WI",
            "state_WV",
            "state_WY",
            "state_YT",
            "state_ZZ",
        ],
    )

    # first time donor
    if first_time == "Yes":
        final_df["first_time_donor"] = 1

    # Occupation
    if occupation == "NOT EMPLOYED":
        final_df["occ_not_emp"] = 1
    elif occupation == "TEACHER":
        final_df["occ_teacher"] = 1
    elif occupation == "RETIRED":
        final_df["occ_retired"] = 1
    elif occupation == "LAWYER":
        final_df["occ_law"] = 1
    elif occupation == "ENGINEER":
        final_df["occ_eng"] = 1
    elif occupation == "PROFESSOR":
        final_df["occ_prof"] = 1
    elif occupation == "SOFTWARE ENGINEER":
        final_df["occ_swe"] = 1
    elif occupation == "PHYSICIAN":
        final_df["occ_dr"] = 1
    elif occupation == "SALES":
        final_df["occ_sales"] = 1
    elif occupation == "CONSULTANT":
        final_df["occ_consult"] = 1
    elif occupation == "MANAGER":
        final_df["occ_manager"] = 1
    elif occupation == "NURSE":
        final_df["occ_nurse"] = 1
    elif occupation == "SELF EMPLOYED":
        final_df["occ_self"] = 1

    # Earmark Type
    if earmark_type == "Bernie":
        final_df["earmarked_bernie"] = 1
    elif earmark_type == "ActBlue":
        final_df["earmarked_actblue"] = 1
    elif earmark_type == "Biden":
        final_df["earmarked_biden"] = 1
    elif earmark_type == "Warren":
        final_df["earmarked_warren"] = 1
    elif earmark_type == "Pete for America":
        final_df["earmarked_pete"] = 1
    elif earmark_type == "DCCC":
        final_df["earmarked_dccc"] = 1
    elif earmark_type == "Stop Republicans":
        final_df["earmarked_stop"] = 1
    elif earmark_type == "Amy for America":
        final_df["earmarked_amy"] = 1
    elif earmark_type == "DSCC":
        final_df["earmarked_dscc"] = 1
    elif earmark_type == "End Citizens United":
        final_df["earmarked_ecup"] = 1

    # State
    if us_state == "AB":
        final_df["state_AB"] = 1
    elif us_state == "AE":
        final_df["state_AE"] = 1
    elif us_state == "AK":
        final_df["state_AK"] = 1
    elif us_state == "AL":
        final_df["state_AL"] = 1
    elif us_state == "AP":
        final_df["state_AP"] = 1
    elif us_state == "AR":
        final_df["state_AR"] = 1
    elif us_state == "AS":
        final_df["state_AS"] = 1
    elif us_state == "AZ":
        final_df["state_AZ"] = 1
    elif us_state == "BC":
        final_df["state_BC"] = 1
    elif us_state == "CA":
        final_df["state_CA"] = 1
    elif us_state == "CO":
        final_df["state_CO"] = 1
    elif us_state == "CT":
        final_df["state_CT"] = 1
    elif us_state == "DC":
        final_df["state_DC"] = 1
    elif us_state == "DE":
        final_df["state_DE"] = 1
    elif us_state == "FL":
        final_df["state_FL"] = 1
    elif us_state == "GA":
        final_df["state_GA"] = 1
    elif us_state == "GU":
        final_df["state_GU"] = 1
    elif us_state == "HI":
        final_df["state_HI"] = 1
    elif us_state == "IA":
        final_df["state_IA"] = 1
    elif us_state == "ID":
        final_df["state_ID"] = 1
    elif us_state == "IL":
        final_df["state_IL"] = 1
    elif us_state == "IN":
        final_df["state_IN"] = 1
    elif us_state == "KS":
        final_df["state_KS"] = 1
    elif us_state == "KY":
        final_df["state_KY"] = 1
    elif us_state == "LA":
        final_df["state_LA"] = 1
    elif us_state == "MA":
        final_df["state_MA"] = 1
    elif us_state == "MB":
        final_df["state_MB"] = 1
    elif us_state == "MD":
        final_df["state_MD"] = 1
    elif us_state == "ME":
        final_df["state_ME"] = 1
    elif us_state == "MI":
        final_df["state_MI"] = 1
    elif us_state == "MN":
        final_df["state_MN"] = 1
    elif us_state == "MO":
        final_df["state_MO"] = 1
    elif us_state == "MP":
        final_df["state_MP"] = 1
    elif us_state == "MS":
        final_df["state_MS"] = 1
    elif us_state == "MT":
        final_df["state_MT"] = 1
    elif us_state == "NB":
        final_df["state_NB"] = 1
    elif us_state == "NC":
        final_df["state_NC"] = 1
    elif us_state == "ND":
        final_df["state_ND"] = 1
    elif us_state == "NE":
        final_df["state_NE"] = 1
    elif us_state == "NH":
        final_df["state_NH"] = 1
    elif us_state == "NJ":
        final_df["state_NJ"] = 1
    elif us_state == "NL":
        final_df["state_NL"] = 1
    elif us_state == "NM":
        final_df["state_NM"] = 1
    elif us_state == "NS":
        final_df["state_NS"] = 1
    elif us_state == "NV":
        final_df["state_NV"] = 1
    elif us_state == "NY":
        final_df["state_NY"] = 1
    elif us_state == "OH":
        final_df["state_OH"] = 1
    elif us_state == "OK":
        final_df["state_OK"] = 1
    elif us_state == "ON":
        final_df["state_ON"] = 1
    elif us_state == "OR":
        final_df["state_OR"] = 1
    elif us_state == "PA":
        final_df["state_PA"] = 1
    elif us_state == "PE":
        final_df["state_PE"] = 1
    elif us_state == "PR":
        final_df["state_PR"] = 1
    elif us_state == "QC":
        final_df["state_QC"] = 1
    elif us_state == "RI":
        final_df["state_RI"] = 1
    elif us_state == "SC":
        final_df["state_SC"] = 1
    elif us_state == "SD":
        final_df["state_SD"] = 1
    elif us_state == "TN":
        final_df["state_TN"] = 1
    elif us_state == "TX":
        final_df["state_TX"] = 1
    elif us_state == "UT":
        final_df["state_UT"] = 1
    elif us_state == "VA":
        final_df["state_VA"] = 1
    elif us_state == "VI":
        final_df["state_VI"] = 1
    elif us_state == "VT":
        final_df["state_VT"] = 1
    elif us_state == "WA":
        final_df["state_WA"] = 1
    elif us_state == "WI":
        final_df["state_WI"] = 1
    elif us_state == "WV":
        final_df["state_WV"] = 1
    elif us_state == "WY":
        final_df["state_WY"] = 1
    elif us_state == "YT":
        final_df["state_YT"] = 1
    elif us_state == "ZZ":
        final_df["state_ZZ"] = 1

    return final_df


def prediction_result(model, data) -> pd.DataFrame:
    # make prediction
    preds = model.predict(data)
    labels = ["Predicted Donation"]

    new_pred = pd.DataFrame(preds, columns=labels)
    return new_pred


def plot_preds(prediction):
    # plot preds with plotly

    # reshape data
    prediction = prediction.T.reset_index()
    prediction.columns = ["Prediction", "Dollars"]

    fig = px.bar(
        prediction,
        x="Prediction",
        y="Dollars",
        color="Prediction",
    )
    fig.update_layout(
        title="Predicted Donation",
        xaxis_title="",
        yaxis_title="Donation",
    )
    # add horizontal line at 125
    fig.add_hline(
        y=22.7,
        line_dash="dot",
        line_color="red",
        annotation_text="Avg Donation",
        annotation_position="bottom right",
    )
    # make y label dollar amount
    fig.update_yaxes(tickprefix="$", tickformat=".0f")
    # set y axis range
    fig.update_yaxes(range=[0, 75])

    return fig
