# Contribution Model API



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

![API Request](https://github.com/papagorgio23/segmentation_api/blob/main/img/predict_api_1.png)




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


#### Predict_CSV

Upload sample csv file `Data_Science_Technical_FEC_Filing_Sample.csv` and it will return the predicted contribution amount for each row.
