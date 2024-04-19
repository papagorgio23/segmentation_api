from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import joblib
import pandas as pd
import numpy as np


from src.utils.functions import (
    add_missing_cols,
    create_features_api,
    create_features,
    features,
)
from src.utils.models import Payload


# load model
model = joblib.load("./models/contribution_model_2024-04-18.pkl")

# init API
app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the ActBlue contribution model API from Sr. Data Scientist Jason Lee"
    }


@app.post("/predict/")
async def predict_json(payload: Payload) -> list:

    df = pd.DataFrame([x.dict() for x in payload.data])
    df = create_features_api(df)
    df[f"state_{df.loc[0, 'contributor_state']}"] = 1
    df = add_missing_cols(df, features)
    preds = model.predict(df[features])

    # create json response object
    response = []
    for i in range(len(preds)):
        resp = {
            "memo_text_description": df.loc[i, "memo_text_description"],
            "contributor_occupation": df.loc[i, "contributor_occupation"],
            "contributor_state": df.loc[i, "contributor_state"],
            "first_time_donor": int(df.loc[i, "first_time_donor"]),
            "predicted_contribution": round(float(preds[i]), 2),
        }
        response.append(resp)
    return response


@app.post("/predict_csv/")
async def predict_csv(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)
    # randomly sample 1,000 rows since the sample file has 400k rows and takes a while to process
    df = df.sample(1000)
    df = create_features(df)
    df = add_missing_cols(df, features)
    df["predicted_contribution"] = model.predict(df[features])

    # Return results as CSV to download
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"},
    )
