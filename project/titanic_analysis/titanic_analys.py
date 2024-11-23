import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

train_data = pd.read_csv("project/titanic_analysis/train.csv")
test_data = pd.read_csv("project/titanic_analysis/test.csv")

age_imputer = SimpleImputer(strategy="median")
train_data["Age"] = age_imputer.fit_transform(train_data[["Age"]])

embarked_imputer = SimpleImputer(strategy="most_frequent")
train_data["Embarked"] = embarked_imputer.fit_transform(
    train_data[["Embarked"]]
).ravel()

train_data.drop(columns=["Cabin"], inplace=True)

# Exploratory Data Analysis (EDA)
sns.countplot(data=train_data, x="Survived")
plt.title("Survival distribution")
plt.show()

sns.histplot(data=train_data, x="Age", kde=True)
plt.title("Age distribution of passengers")
plt.show()

sns.countplot(data=train_data, x="Sex", hue="Survived")
plt.title("Survival rate by gender")
plt.show()

numeric_columns = train_data.select_dtypes(include=["number"])
corr_matrix = numeric_columns.corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation of features")
plt.show()

# Data Transformation (Feature Engineering)
label_encoder = LabelEncoder()
train_data["Sex"] = label_encoder.fit_transform(train_data["Sex"])
train_data["Embarked"] = label_encoder.fit_transform(train_data["Embarked"])

train_data["FamilySize"] = train_data["SibSp"] + train_data["Parch"] + 1

train_data.drop(columns=["Name", "Ticket"], inplace=True)

scaler = StandardScaler()
train_data[["Age", "Fare"]] = scaler.fit_transform(train_data[["Age", "Fare"]])

# Building classification models
X = train_data.drop(columns=["Survived"])
y = train_data["Survived"]

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

X_train, X_val, y_train, y_val = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# A function for training and evaluating the model
def evaluate_model(model):
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    print(f"\n{model.__class__.__name__}:")
    print(classification_report(y_val, preds))
    return accuracy_score(y_val, preds)


# Decision Tree Classifier
dt_model = DecisionTreeClassifier(random_state=42)
dt_param_grid = {"max_depth": [None, 5, 10], "min_samples_split": [2, 5]}
dt_grid_search = GridSearchCV(dt_model, dt_param_grid, cv=5)
dt_grid_search.fit(X_train, y_train)
print(f"Best parameters for Decision Tree: {dt_grid_search.best_params_}")
evaluate_model(dt_grid_search.best_estimator_)

# Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42)
rf_param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [None, 10],
    "min_samples_split": [2, 5],
}
rf_grid_search = GridSearchCV(rf_model, rf_param_grid, cv=5)
rf_grid_search.fit(X_train, y_train)
print(f"Best parameters for Random Forest: {rf_grid_search.best_params_}")
evaluate_model(rf_grid_search.best_estimator_)

# Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=2000)
lr_param_grid = {"C": [0.01, 0.1, 1.0], "solver": ["liblinear"]}
lr_grid_search = GridSearchCV(lr_model, lr_param_grid, cv=5)
lr_grid_search.fit(X_train, y_train)
print(f"Best parameters for Logistic Regression: {lr_grid_search.best_params_}")
evaluate_model(lr_grid_search.best_estimator_)

# Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_param_grid = {
    "n_estimators": [50, 100],
    "learning_rate": [0.01, 0.1],
    "max_depth": [3, 5],
}
gb_grid_search = GridSearchCV(gb_model, gb_param_grid, cv=5)
gb_grid_search.fit(X_train, y_train)
print(f"Best parameters for Gradient Boosting: {gb_grid_search.best_params_}")
evaluate_model(gb_grid_search.best_estimator_)

# Building a regression model
reg_data = train_data.dropna(subset=["Age"])
reg_target = reg_data["Age"]
reg_features = reg_data.drop(columns=["Age", "Survived"])

X_train_reg, X_val_reg, y_train_reg, y_val_reg = train_test_split(
    reg_features, reg_target, test_size=0.2, random_state=42
)

# Linear Regression
lr_reg_model = LinearRegression()
lr_reg_model.fit(X_train_reg, y_train_reg)
lr_reg_preds = lr_reg_model.predict(X_val_reg)
print("\nLinear Regression:")
print(f"RMSE: {mean_squared_error(y_val_reg, lr_reg_preds, squared=False):.2f}")

# Random Forest Regressor
rf_reg_model = RandomForestRegressor(random_state=42)
rf_reg_param_grid = {"n_estimators": [50, 100], "max_depth": [None, 10]}
rf_reg_grid_search = GridSearchCV(rf_reg_model, rf_reg_param_grid, cv=5)
rf_reg_grid_search.fit(X_train_reg, y_train_reg)
print(f"Best parameters for Random Forest Regressor: {rf_reg_grid_search.best_params_}")
rf_reg_preds = rf_reg_grid_search.predict(X_val_reg)
print("\nRandom Forest Regressor:")
print(f"RMSE: {mean_squared_error(y_val_reg, rf_reg_preds, squared=False):.2f}")
