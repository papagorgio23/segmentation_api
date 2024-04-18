import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from time import time
from datetime import datetime

from utils.functions import create_features, features


print(
    """
--------------------------------------------------------

 
      _              _   ______   __                  
     / \            / |_|_   _ \ [  |                 
    / _ \     .---.`| |-' | |_) | | | __   _   .---.  
   / ___ \   / /'`\]| |   |  __'. | |[  | | | / /__\\ 
 _/ /   \ \_ | \__. | |, _| |__) || | | \_/ |,| \__., 
|____| |____|'.___.'\__/|_______/[___]'.__.'_/ '.__.' 
                                                      
          
--------------------------------------------------------



Training Model to predict contributions by individuals to political committees



Loading Data...
"""
)

# load training data
df = pd.read_csv("./data/Data_Science_Technical_FEC_Filing_Sample.csv")

print("Data Shape: ", df.shape)
print("")
print("")
print(df.info())


# Check missing values
print("\nChecking for missing values...")
print(df.isnull().sum())


# Create features
print("\nFeature Engineering...")
df = create_features(df)
print("New Data Shape: ", df.shape)
print("")
print("Features Used in Model:")
print(features)


# Split data
print("\nPreparing Model Data...")
# Define target and features
target = "contribution_amount"
X = df[features]
y = df[target]

# split data into training and testing sets (30% holdout for testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# split training data into training and validation sets
# - 49% of full dataset will be used for training
# - 21% of full dataset will be used for validation during training process
# - 30% of full dataset will be used for testing
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.3, random_state=42
)


# init model and set hyperparameters
model = xgb.XGBRegressor(
    n_estimators=1000,
    seed=123,
    objective="reg:squarederror",
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    early_stopping_rounds=10,
    gamma=1,
    reg_alpha=0.1,
    reg_lambda=1,
    n_jobs=-1,
    random_state=42,
)

# start timer
start = time()
# Train model
print("\nTraining Model...")
model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    verbose=True,
)
time_elapsed = time() - start
# set timer for model training
print("\nModel Training Complete!")
print(f"Time Elapsed: {round(time_elapsed, 2)} seconds")

# predict on test set
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"\nMean Squared Error: {round(mse)}")

print("\n\nMost Important Features:")
feature_import = pd.DataFrame(
    model.feature_importances_, index=model.feature_names_in_, columns=["importance"]
)
print(feature_import.sort_values(by="importance", ascending=False)[:20])


# save model
print("\nSaving Model...")
model.save_model(f"./models/contribution_model_{datetime.now().date()}.json")

print("\nModel Saved!")
print("\nTraining Complete!")
print("\n--------------------------------------------------------")
