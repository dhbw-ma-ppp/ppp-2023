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
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import ensemble

def initialazion():
    # Read the data
    working_dir = Path(os.getcwd()).parent.absolute().parent.absolute()
    train = pd.read_csv(str(working_dir) + "/data/titanic_train.csv")
    test = pd.read_csv(str(working_dir) + "/data/titanic_test.csv")

    # Preprocess the data
    train = preprocess(train)
    test = preprocess(test)

    # Split the data into features and labels
    train_labels = train["Survived"]
    train_features = train.drop("Survived", axis=1)
    test_labels = test["Survived"]
    test_features = test.drop("Survived", axis=1)

    # Train the model
    model = train_model(train_features, train_labels)

    # Evaluate the model
    evaluate_model(model, test_features, test_labels) # the arguments can be changed to train_features, train_labels to evaluate the model on the training set

def preprocess(data):
    # Drop the unnecessary columns, this means that only the following columns are kept: Survived, Sex, Age, SibSp, Parch, Fare, Embarked
    data = data.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1)

    # Convert categorical data to one-hot encoding
    data = pd.get_dummies(data) #dummies means

    # Fill in missing values
    data = data.fillna(data.mean())

    return data

def train_model(features, labels):
    # Create the model
    model = ensemble.RandomForestClassifier(n_estimators=100)

    # Train the model
    model.fit(features, labels)

    return model

def evaluate_model(model, features, labels):
    # Predict the labels
    predictions = model.predict(features)

    # Calculate the MCC score
    mcc = metrics.matthews_corrcoef(labels, predictions)
    print("MCC score:", mcc)

    # Calculate the confusion matrix
    confusion = metrics.confusion_matrix(labels, predictions)
    print("Confusion matrix:")
    print(confusion)
    #confusion matrix as plot
    fig, ax = plt.subplots()
    ax.matshow(confusion, cmap=plt.cm.Blues)
    for i in range(confusion.shape[0]):
        for j in range(confusion.shape[1]):
            ax.text(x=j, y=i, s=confusion[i, j], va='center', ha='center')
    plt.xlabel('predicted label')
    plt.ylabel('true label')
    plt.show()
    accuracy = metrics.accuracy_score(labels, predictions)
    print("Accuracy:", accuracy)

initialazion()