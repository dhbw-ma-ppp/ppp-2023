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

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import matthews_corrcoef
from sklearn.impute import KNNImputer
import pandas as pd

data = pd.read_csv("../../data/titanic_train.csv")
data['Sex'] = data['Sex'].apply(lambda x: 1 if 'female' in x else 0)
del data['PassengerId'], data['Embarked'], data['Ticket'], data['Name'], data['Parch'], data['SibSp'], data['Cabin']
values = []

def compute(neighbor=5, comp_data = data, depth=5):
    imputer = KNNImputer(n_neighbors = neighbor)
    missing_columns = comp_data.isnull().sum()
    for key in [index for index in missing_columns.index if missing_columns[index] > 0]:
        comp_data[key] = imputer.fit_transform(comp_data[key].values.reshape(-1,1))
    features = comp_data.iloc[:, 1:]
    label = comp_data[['Survived']]
    result = []
    x_train, x_test, y_train, y_test = train_test_split(features,label,test_size=0.2, stratify=label)
    model = tree.DecisionTreeClassifier(max_depth=depth)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    res = matthews_corrcoef(y_test, y_pred)
    return res

for a in range(1,4):
    for i in range(1,50):
        values.append(max([compute(i) for j in range(1,10)]))
    neighbor = values.index(max(values))+1
    values = []
    for i in range(1,50):
        values.append(max([compute(neighbor, data, i) for j in range(1,10)]))
    depth = values.index(max(values))+1
    print(compute(neighbor, data, depth))
    print(compute())
