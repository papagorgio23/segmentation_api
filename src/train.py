import pandas as pd

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
print("")
print("Checking for missing values...")
print(df.isnull().sum())
print("")


# Create features
print("Feature Engineering...")
df = create_features(df)
print("New Data Shape: ", df.shape)
print("")
print("Features Used in Model:")
print(features)
