# Prepare an analysis of the titanic dataset (data/titanic.csv).
# You are interested in determining factors that lead to death or survival of passengers.
# However, before actually training an ML model to predict death or survival, you should make
# yourself familiar with the data.
#
# Look into which features are available, what types of features these are, whether
# values are missing and how to deal with them, etc.
# You can then continue to create some visualizations of things you think might be interesting or relevant
# in predicting survival, or just generally useful to know about the dataset.
# The output should not just be prints of numbers or figures, but also some explanatory text of
# what you have been analysing, and which conclusions you can draw from the different steps of your analysis.
#
# You can do all of this in a Jupyter Notebook, embedding analysis, code and explanations in a single document.
# Alternatively you can create a separate script for the analysis, and then list results, figures and explanations
# either in the PR directly, or in some form of pdf/word/markdown/... document.
#
# For this exercise I very much encourage you to work together to come up with ideas of which
# calculations/plots/... might be interesting to analyse. You will find very many such analyses online
# for the titanic data, but I would recommend trying to think of your own ideas first, and only later
# look for more inspiration online.

from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

path = Path(__file__).parents[2] / "data" / "titanic.csv"
data = pd.read_csv(path)

#Dropping duplicates
print(f"Shape at the beginning:\n{data.shape}")
data.drop_duplicates(inplace = True)
print(f"\nShape after dropping duplicates:\n{data.shape}\n")

print('-' * 30)

#Treating null values:
print(f"\nCount of null arguments:\n{data.isnull().sum()}")
#Age: null replaced with average age
data["Age"] = data["Age"].fillna(int(data["Age"].mean())) #Still have to converte data to age!!
#Cabin: Mostly empty: data is unnecessary and can be deleted
data.drop(columns = ["Cabin"], inplace = True)
#Embarked: Only 2 null Arguments, will be replaced by 'S'
data["Embarked"] = data["Embarked"].fillna('S')
print(f"\nCount of null arguemnts after fix:\f{data.isnull().sum()}\n")

print('-' * 30)

#Treating non numeric values:
print(f"\nTypes of values:\n{data.dtypes}")
#Name: Will be replaced by length of name string
data["Name"] = data["Name"].map(lambda name: len(name))
#Sex: Nothing to change, data only contains "female" and "male"
#Ticket: Will be replaced by length of ticket string
data["Ticket"] = data["Ticket"].map(lambda ticket: len(ticket))
#Embarked: Nothing to change, data only contains "S", "C", "Q"
print(f"\nTypes of values after fix:\n{data.dtypes}")

print('-' * 30)

#Treating SibSp and Parch:
#Sum those two collumns and write result into Fam
def sum_family(s: pd.Series) -> pd.Series:
    s["Fam"] = s["SibSp"] + s["Parch"]
    return s
data = data.apply(sum_family, axis = 1).drop("SibSp", axis = 1).drop("Parch", axis = 1)
print(f"\nTypes of values after summing SibSp and Parch into Fam:\n{data.dtypes}")


_SURVIVALRATE_BY_COLUMNS_Discrete = [
    "Pclass",
    "Sex",
    "Embarked",
]

for col in _SURVIVALRATE_BY_COLUMNS_Discrete:
    print('-' * 30)
    plot_data = data.groupby([col], as_index = False)["Survived"].mean()
    print(f"\nSurivalrate by {col}:\n{plot_data}\n")
    sns.barplot(data = plot_data, x = col, y = "Survived")
    plt.title(f"Survivalrate by {col}")
    plt.show()

_SURVIVALRATE_BY_COLUMNS_Continuous = [
    "PassengerId",
    "Name",
    "Age",
    "Ticket",
    "Fare",
    "Fam",
]

for col in _SURVIVALRATE_BY_COLUMNS_Continuous:
    sns.violinplot(data = data[["Survived", col]], x = "Survived", y = col)
    plt.title(f"Survivalrate by {col}")
    plt.show()