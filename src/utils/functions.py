import pandas as pd
import numpy as np


## Features
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


# Function to create all the new features
def create_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create features for the model
    """
    # create flag for what the donation is earmarked for
    data["earmarked_bernie"] = np.where(
        data["memo_text_description"].str.contains("BERNIE"), 1, 0
    )
    data["earmarked_actblue"] = np.where(
        data["memo_text_description"].str.contains("ActBlue"), 1, 0
    )
    data["earmarked_biden"] = np.where(
        data["memo_text_description"].str.contains("BIDEN"), 1, 0
    )
    data["earmarked_warren"] = np.where(
        data["memo_text_description"].str.contains("WARREN"), 1, 0
    )
    data["earmarked_pete"] = np.where(
        data["memo_text_description"].str.contains("PETE FOR AMERICA"), 1, 0
    )
    data["earmarked_dccc"] = np.where(
        data["memo_text_description"].str.contains("DCCC"), 1, 0
    )
    data["earmarked_stop"] = np.where(
        data["memo_text_description"].str.contains("STOP REPUBLICANS"), 1, 0
    )
    data["earmarked_amy"] = np.where(
        data["memo_text_description"].str.contains("AMY FOR AMERICA"), 1, 0
    )
    data["earmarked_dscc"] = np.where(
        data["memo_text_description"].str.contains("DSCC"), 1, 0
    )
    data["earmarked_ecup"] = np.where(
        data["memo_text_description"].str.contains("END CITIZENS"), 1, 0
    )

    # create flag for occupation of donor
    data["occ_not_emp"] = np.where(
        data["contributor_occupation"].str.contains("NOT EMPLOYED"), 1, 0
    )
    data["occ_teacher"] = np.where(
        data["contributor_occupation"].str.contains("TEACHER"), 1, 0
    )
    data["occ_retired"] = np.where(
        data["contributor_occupation"].str.contains("RETIRED"), 1, 0
    )
    data["occ_law"] = np.where(
        data["contributor_occupation"].str.contains("ATTORNEY"), 1, 0
    ) | np.where(data["contributor_occupation"].str.contains("LAWYER"), 1, 0)
    data["occ_eng"] = np.where(data["contributor_occupation"] == "ENGINEER", 1, 0)
    data["occ_prof"] = np.where(
        data["contributor_occupation"].str.contains("PROFESSOR"), 1, 0
    )
    data["occ_swe"] = np.where(
        data["contributor_occupation"].str.contains("SOFTWARE"), 1, 0
    )
    data["occ_dr"] = np.where(
        data["contributor_occupation"].str.contains("PHYSICIAN"), 1, 0
    )
    data["occ_sales"] = np.where(
        data["contributor_occupation"].str.contains("SALES"), 1, 0
    )
    data["occ_consult"] = np.where(
        data["contributor_occupation"].str.contains("CONSULTANT"), 1, 0
    )
    data["occ_manager"] = np.where(
        data["contributor_occupation"].str.contains("MANAGER"), 1, 0
    )
    data["occ_nurse"] = np.where(
        data["contributor_occupation"] == "RN", 1, 0
    ) | np.where(data["contributor_occupation"].str.contains("NURSE"), 1, 0)
    data["occ_self"] = np.where(
        data["contributor_occupation"].str.contains("SELF"), 1, 0
    )

    # Create flag for if it's a first time donor by grouping by contributor name
    # create new column with first name and last name
    if "first_time_donor" not in data.columns:
        data["full_name"] = (
            data["contributor_first_name"] + " " + data["contributor_last_name"]
        )
        data = data.sort_values(by=["contribution_date", "full_name"])
        data["num_donations"] = data.groupby("full_name")[
            "contribution_amount"
        ].transform("count")
        data["first_time_donor"] = np.where(data["num_donations"] == 1, 1, 0)

    # dummy variables for state
    final_data = pd.get_dummies(
        data, columns=["contributor_state"], drop_first=True, prefix="state", dtype=int
    )

    return final_data


# Function to create all the new features for the API
def create_features_api(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create features for the model
    """
    # create flag for what the donation is earmarked for
    data["earmarked_bernie"] = np.where(
        data["memo_text_description"].str.contains("BERNIE"), 1, 0
    )
    data["earmarked_actblue"] = np.where(
        data["memo_text_description"].str.contains("ActBlue"), 1, 0
    )
    data["earmarked_biden"] = np.where(
        data["memo_text_description"].str.contains("BIDEN"), 1, 0
    )
    data["earmarked_warren"] = np.where(
        data["memo_text_description"].str.contains("WARREN"), 1, 0
    )
    data["earmarked_pete"] = np.where(
        data["memo_text_description"].str.contains("PETE FOR AMERICA"), 1, 0
    )
    data["earmarked_dccc"] = np.where(
        data["memo_text_description"].str.contains("DCCC"), 1, 0
    )
    data["earmarked_stop"] = np.where(
        data["memo_text_description"].str.contains("STOP REPUBLICANS"), 1, 0
    )
    data["earmarked_amy"] = np.where(
        data["memo_text_description"].str.contains("AMY FOR AMERICA"), 1, 0
    )
    data["earmarked_dscc"] = np.where(
        data["memo_text_description"].str.contains("DSCC"), 1, 0
    )
    data["earmarked_ecup"] = np.where(
        data["memo_text_description"].str.contains("END CITIZENS"), 1, 0
    )

    # create flag for occupation of donor
    data["occ_not_emp"] = np.where(
        data["contributor_occupation"].str.contains("NOT EMPLOYED"), 1, 0
    )
    data["occ_teacher"] = np.where(
        data["contributor_occupation"].str.contains("TEACHER"), 1, 0
    )
    data["occ_retired"] = np.where(
        data["contributor_occupation"].str.contains("RETIRED"), 1, 0
    )
    data["occ_law"] = np.where(
        data["contributor_occupation"].str.contains("ATTORNEY"), 1, 0
    ) | np.where(data["contributor_occupation"].str.contains("LAWYER"), 1, 0)
    data["occ_eng"] = np.where(data["contributor_occupation"] == "ENGINEER", 1, 0)
    data["occ_prof"] = np.where(
        data["contributor_occupation"].str.contains("PROFESSOR"), 1, 0
    )
    data["occ_swe"] = np.where(
        data["contributor_occupation"].str.contains("SOFTWARE"), 1, 0
    )
    data["occ_dr"] = np.where(
        data["contributor_occupation"].str.contains("PHYSICIAN"), 1, 0
    )
    data["occ_sales"] = np.where(
        data["contributor_occupation"].str.contains("SALES"), 1, 0
    )
    data["occ_consult"] = np.where(
        data["contributor_occupation"].str.contains("CONSULTANT"), 1, 0
    )
    data["occ_manager"] = np.where(
        data["contributor_occupation"].str.contains("MANAGER"), 1, 0
    )
    data["occ_nurse"] = np.where(
        data["contributor_occupation"] == "RN", 1, 0
    ) | np.where(data["contributor_occupation"].str.contains("NURSE"), 1, 0)
    data["occ_self"] = np.where(
        data["contributor_occupation"].str.contains("SELF"), 1, 0
    )

    return data


def add_missing_cols(df, predictors):
    """Add missing columns to dataframe.

    Parameters
    ----------
    df : dataframe
        dataframe to add missing columns to
    predictors : list
        list of columns to add

    Returns
    -------
    df : dataframe
        dataframe with added columns
    """
    for col in predictors:
        if col not in df.columns:
            df[col] = 0
    return df
