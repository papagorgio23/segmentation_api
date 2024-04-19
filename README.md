# Contribution Model API


## Demo Model

This is a demo model that predicts the contribution amount based on the following features:

- First time donor (Yes/No)
- Purpose of Donation (Memo Text Description)
- Donor Occupation (Contributor Occupation)
- Donor State (Contributor State)

View the demo model [here](https://papagorgio23-segmentation-api-appapp-q4hb3q.streamlit.app/)



## Build Docker Image

```bash
make docker-build 
```


## Run Docker Image

```bash
make docker-run
```



### API Docs

When docker is running: http://localhost/docs


#### API Endpoints

predict: http://localhost/predict

```json
{
  "data": [
    {
      "memo_text_description": "BIDEN",
      "contributor_occupation": "TEACHER",
      "contributor_state": "CA",
      "first_time_donor": 1
    },
    {
      "memo_text_description": "AMY",
      "contributor_occupation": "PHYSICIAN",
      "contributor_state": "FL",
      "first_time_donor": 0
    }
  ]
}
```

![API Request](https://github.com/papagorgio23/segmentation_api/blob/main/img/predict_api_2.png)




Response:

```json
[
  {
    "memo_text_description": "BIDEN",
    "contributor_occupation": "TEACHER",
    "contributor_state": "CA",
    "first_time_donor": 1,
    "predicted_contribution": 30.94
  },
  {
    "memo_text_description": "AMY",
    "contributor_occupation": "PHYSICIAN",
    "contributor_state": "FL",
    "first_time_donor": 0,
    "predicted_contribution": 143.12
  }
]
```


![API Request](https://github.com/papagorgio23/segmentation_api/blob/main/img/predict_api_4.png)


#### Predict_CSV

Upload sample csv file `Data_Science_Technical_FEC_Filing_Sample.csv` and it will return the predicted contribution amount for each row. You can download the results as a csv file.


![API Request](https://github.com/papagorgio23/segmentation_api/blob/main/img/predict_csv_api_1.png)


![API Request](https://github.com/papagorgio23/segmentation_api/blob/main/img/predict_csv_api_2.png)
