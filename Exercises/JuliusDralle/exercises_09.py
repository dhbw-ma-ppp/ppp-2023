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
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import matthews_corrcoef


path_here = pathlib.Path(__file__).parent
path_dir_exercises = path_here.parent
path_dir_root = path_dir_exercises.parent
path_dir_data = path_dir_root / "data"

df = pd.read_csv(path_dir_data / "titanic_train.csv" )


#print(df["Embarked"])


df['Sex'] = df['Sex'].replace(['female','male'],[0,1])
df['Embarked'] = df['Embarked'].replace(['S','C','Q'],[0,1,2])
 
#print(df)

label = df[["Survived"]]
#features = df.drop(columns = ['Name','Ticket','PassengerId','Survived','Embarked','Cabin'])
features = df.drop(columns = ['Name','Ticket','PassengerId','Survived','Cabin'])

features_train, features_validate, label_train, label_validate = train_test_split(features, label, test_size=0.2, stratify=label)

classifier = tree.DecisionTreeClassifier(max_depth=8)
classifier.fit(features_train, label_train)
label_predicted = classifier.predict(features_validate)
label_predicted_ontraindata = classifier.predict(features_train)

print("Validierung: ",matthews_corrcoef(label_validate, label_predicted))
print("Train: ",matthews_corrcoef(label_train, label_predicted_ontraindata))


# TEST Data area

df_test = pd.read_csv(path_dir_data / "titanic_test.csv" )
df_test['Embarked'] = df_test['Embarked'].replace(['S','C','Q'],[0,1,2])
df_test['Sex'] = df_test['Sex'].replace(['female','male'],[0,1])
label_test = df_test['Survived']
features_test = df_test.drop(columns = ['Name','Ticket','PassengerId','Survived','Cabin'])

label_predicted_test = classifier.predict(features_test)


print("TEST: ",matthews_corrcoef(label_test, label_predicted_test))

