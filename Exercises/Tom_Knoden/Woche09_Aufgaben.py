import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef

train_file_path = Path('data/train.csv')
train_data = pd.read_csv(train_file_path)


#feature selection and preprocessing
#using Pclass, Sex, Age, and Embarked as features
features = ['Pclass', 'Sex', 'Age', 'Embarked']
X = train_data[features]
X = pd.get_dummies(X)  # Convert categorical variables to dummy/indicator variables
y = train_data['Survived']

#splitting the training data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

#now I'm training a RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#some predictions on the validation set
y_val_pred = model.predict(X_val)

#evaluating the models with Matthews Correlation Coefficient
mcc_score = matthews_corrcoef(y_val, y_val_pred)
print(f'Matthews Correlation Coefficient on the validation set: {mcc_score}')

#final evaluation
test_file_path = Path('data/test.csv')
test_data = pd.read_csv(test_file_path)

#preprocessing the test data similarly to the training data
X_test = test_data[features]
X_test = pd.get_dummies(X_test)

#making predictions
y_test_pred = model.predict(X_test)

#evaluating the model on the provided test set
test_labels_file_path = Path('data/test_labels.csv')
test_labels = pd.read_csv(test_labels_file_path)['Survived']
test_mcc_score = matthews_corrcoef(test_labels, y_test_pred)
print(f'Matthews Correlation Coefficient on the test set: {test_mcc_score}')
