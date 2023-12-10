import pandas as pd
import pathlib
import matplotlib as plt
import os




#Importing the data
here = pathlib.Path(os.path.abspath(''))
exercise_dir = here.parent
data_dir = exercise_dir.parent / "data"

titanic_df = pd.read_csv("titanic.csv")
print(titanic_df)
