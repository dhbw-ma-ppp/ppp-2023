import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

root_dir = Path(__file__).absolute().parents[2]
input_file_path = root_dir / "data" / "titanic.csv"
titanic_data = pd.read_csv(input_file_path)


#Basic Information
print("Basic Information:")
print("The dataset contains information about passengers on the Titanic.")
print("It includes details such as age, sex, passenger class, and survival status.")
print(titanic_data.info())
print("\n")

#Summary Statistics for Numerical Columns
print("Summary Statistics for Numerical Columns:")
print("Here are the summary statistics for numerical columns in the dataset.")
print(titanic_data.describe())
print("\n")

#Missing Values
print("Missing Values:")
print("Checking for missing values in the dataset.")
print(titanic_data.isnull().sum())
print("\n")

#Survival Rate
print("Survival Rate:")
print("Analyzing the overall survival rate of passengers.")
survival_count = titanic_data['Survived'].value_counts()
survival_percentage = survival_count / len(titanic_data) * 100
print(survival_percentage)
survival_percentage.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Survival Percentage')
plt.xticks(rotation=0)
plt.show()
print("\n")

#Survival Rate by Pclass
print("Survival Rate by Pclass:")
print("Analyzing the survival rate based on passenger class (Pclass).")
pclass_survival = titanic_data.groupby(['Pclass', 'Survived']).size().unstack()
pclass_survival_percentage = pclass_survival.div(pclass_survival.sum(axis=1), axis=0) * 100
print(pclass_survival_percentage)
pclass_survival_percentage.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Percentage by Pclass')
plt.xticks(rotation=0)
plt.show()
print("\n")

#Survival Rate by Sex
print("Survival Rate by Sex:")
print("Analyzing the survival rate based on gender (Sex).")
sex_survival = titanic_data.groupby(['Sex', 'Survived']).size().unstack()
sex_survival_percentage = sex_survival.div(sex_survival.sum(axis=1), axis=0) * 100
print(sex_survival_percentage)
sex_survival_percentage.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Percentage by Sex')
plt.xticks(rotation=0)
plt.show()
print("\n")

#Survival Rate by Age group
print("Survival Rate by Age Group:")
print("Analyzing the survival rate based on age groups.")
titanic_data['AgeGroup'] = pd.cut(titanic_data['Age'], bins=[0, 18, 35, 50, 80], labels=['0-18', '19-35', '36-50', '51-80'])
age_group_survival = titanic_data.groupby(['AgeGroup', 'Survived']).size().unstack()
age_group_survival_percentage = age_group_survival.div(age_group_survival.sum(axis=1), axis=0) * 100
print(age_group_survival_percentage)
age_group_survival_percentage.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Percentage by Age Group')
plt.xticks(rotation=0)
plt.show()
print("\n")

#Survival Rate by Embarked
print("Survival Rate by Embarked:")
print("Analyzing the survival rate based on the port of embarkation (Embarked).")
embarked_survival = titanic_data.groupby(['Embarked', 'Survived']).size().unstack()
embarked_survival_percentage = embarked_survival.div(embarked_survival.sum(axis=1), axis=0) * 100
print(embarked_survival_percentage)
embarked_survival_percentage.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'])
plt.title('Survival Percentage by Embarked')
plt.xticks(rotation=0)
plt.show()
print("\n")
