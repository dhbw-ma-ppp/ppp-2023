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

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

input_file_path = Path('data/titanic.csv')
titanic_data = pd.read_csv(input_file_path)

#all the basic information
print(titanic_data.info())

#summary statistics for numerical columns
print(titanic_data.describe())

#Checking for missing values
print(titanic_data.isnull().sum())

#survival rate
survival_count = titanic_data['Survived'].value_counts()
survival_count.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Survival Count')
plt.xticks(rotation=0)
plt.show()

#survival rate by Pclass
pclass_survival = titanic_data.groupby(['Pclass', 'Survived']).size().unstack()
pclass_survival.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Count by Pclass')
plt.xticks(rotation=0)
plt.show()

#survival rate by Sex
sex_survival = titanic_data.groupby(['Sex', 'Survived']).size().unstack()
sex_survival.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Count by Sex')
plt.xticks(rotation=0)
plt.show()

#survival rate by Age group
titanic_data['AgeGroup'] = pd.cut(titanic_data['Age'], bins=[0, 18, 35, 50, 80], labels=['0-18', '19-35', '36-50', '51-80'])
age_group_survival = titanic_data.groupby(['AgeGroup', 'Survived']).size().unstack()
age_group_survival.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Count by Age Group')
plt.xticks(rotation=0)
plt.show()

#survival rate by Embarked
embarked_survival = titanic_data.groupby(['Embarked', 'Survived']).size().unstack()
embarked_survival.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Count by Embarked')
plt.xticks(rotation=0)
plt.show()
