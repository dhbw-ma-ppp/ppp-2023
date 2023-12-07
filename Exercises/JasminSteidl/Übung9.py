# This is the continuation of last weeks exercise.
# After having analysed the Titanic Dataset, you should now prepare a machine
# learning model to predict whether passengers will survive.
#
# It is entirely up to you which algorithm and feature engineering to use.
# I do recommend using some of the algorithms available in sklearn, but if you would 
# like to use another library that's also ok. It's a good idea to try and evaluate different algorithms,
# and different pre-processing/cleaning/feature-generation options if you have the time.
#
# I have split the training data into a train- and a test-set already. These can be found as separate files 
# in the `data`-directory. You should only use the training set throughout your entire development -- feel free 
# to use cross-validation or split the training set into a train- and a validation set again.
# Once you have developed a final model, you should evaluate this model on the test set I've provided,
# and report the MCC score for the test set in the title of your PR. You should **not** evaluate the test
# set more than once for this initial submission!
#
# If you decide to change your code after code-review, you can report new values in the comments, but
# leave the initial MCC in the title unchanged.

import pathlib
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import matthews_corrcoef
from sklearn.ensemble import RandomForestClassifier

root_dir = pathlib.Path().absolute().parents[1]
with open(root_dir / "data" / "titanic_train.csv", "r") as ifile:
    unprocessed_data = pd.read_csv(ifile)


def preprocess_data(data):
    data = data.drop(columns=data.columns[[0, 3, 6, 7, 8, 9, 10, 11]])

    data = data.replace("female", 0)
    data = data.replace("male", 1)

    average_age = data.Age.mean()

    data.fillna(average_age, inplace=True)

    return data


data = preprocess_data(unprocessed_data)
x = data.drop(columns="Survived")
y = data[["Survived"]]

param_grid = {
    'max_depth': [2, 5, 10, 20, 30, 50, 75, 100],
    'min_samples_split':  [2, 10, 50, 75, 100]
}

grid = GridSearchCV(RandomForestClassifier(), param_grid, n_jobs=-1, cv=5, scoring='matthews_corrcoef', verbose=1)

grid.fit(x, y.Survived.ravel())

print(grid.best_score_)
print(grid.best_params_)

print(f"MCC for Train csv: {matthews_corrcoef(y, grid.predict(x))}")

with open(root_dir / "data" / "titanic_test.csv", "r") as ifile:
    test_data = pd.read_csv(ifile)

processed_test_data = preprocess_data(test_data)

x = processed_test_data.drop(columns="Survived") 
y = processed_test_data[["Survived"]]
print((matthews_corrcoef(y, grid.predict(x))))