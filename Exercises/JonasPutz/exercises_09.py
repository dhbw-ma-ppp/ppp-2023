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

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import cross_val_score

def prepare_data(path: Path) -> pd.DataFrame:
    """ Function to prepare the dataframe from an input path"""

    dataframe = pd.read_csv(path)

    #convertion too numeric values:
    dataframe["Sex"] = dataframe["Sex"].map(lambda sex: {"female": 0, "male": 1}[sex])
    #filling na values:
    dataframe["Age"].fillna(dataframe["Age"].mean(), inplace = True)
    
    def sum_family(s: pd.Series) -> pd.Series:
        s["Fam"] = s["SibSp"] + s["Parch"]
        return s
    
    dataframe = dataframe.apply(sum_family, axis = 1)

    #only these collumns will be analysed
    return dataframe[["Survived", "Sex", "Pclass", "Age", "Fam"]]

#read the train csv
train_df = prepare_data(Path(__file__).parents[2] / "data" / "titanic_train.csv")

x = train_df.drop(columns = "Survived")
y = train_df[["Survived"]]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, stratify = y)

#finding best max depth
mean_scores = []
for depth in [2, 3, 4, 5, 6, 7, 8, 9, 10, 30]:
    classifier = tree.DecisionTreeClassifier(max_depth=depth)
    scores = cross_val_score(classifier, x_train, y_train, cv=3, scoring='matthews_corrcoef')
    mean_scores.append((depth, scores.mean(), scores.std()))

print(f"Cross validation:\n{mean_scores}")

best_depth = max(mean_scores, key = lambda val: val[1])[0]
print(f"Best score with max_depth: {max(mean_scores, key = lambda val: val[1])[0]}")


#build decision tree with now found best max_depth
classifier = tree.DecisionTreeClassifier(max_depth = best_depth)
classifier.fit(x, y)
print(f"MCC for Train csv: {matthews_corrcoef(y, classifier.predict(x))}")

#use this classifier on the test csv
test_df = prepare_data(Path(__file__).parents[2] / "data" / "titanic_test.csv")
x = test_df.drop(columns = "Survived")
y = test_df[["Survived"]]
print(f"MCC for Test csv: {matthews_corrcoef(y, classifier.predict(x))}")