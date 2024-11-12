import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


train = pd.read_csv(
    "C:/Users/denis/OneDrive/Рабочий стол/Python/spbu-python-course-1/project/dataset/train.csv"
)
test = pd.read_csv(
    "C:/Users/denis/OneDrive/Рабочий стол/Python/spbu-python-course-1/project/dataset/test.csv"
)

data = pd.concat([train, test], ignore_index=True)

data["Survived"] = data["Survived"].astype("category")
data["Pclass"] = data["Pclass"].astype("category")
data["Sex"] = data["Sex"].astype("category")

print(data.describe())

print(data["Pclass"].value_counts())

age_stats = data.groupby(["Pclass", "Sex"])["Age"].mean()
print(age_stats)

youngest = age_stats.idxmin(), age_stats.min()
oldest = age_stats.idxmax(), age_stats.max()
print("The Youngest:", youngest)
print("The oldest:", oldest)

survivors_with_k = data[(data["Survived"] == 1) & (data["Name"].str.startswith("K"))]
survivors_with_k_sorted = survivors_with_k.sort_values(by="Fare", ascending=False)

print("Passanger paid more than all:", survivors_with_k_sorted.iloc[0]["Name"])
print("Passanger paid less than all:", survivors_with_k_sorted.iloc[-1]["Name"])

data["Relatives"] = data["SibSp"] + data["Parch"]
max_relatives = data[data["Survived"] == 1]["Relatives"].max()
print("Max relatives:", max_relatives)

with_cabin = data[data["Cabin"].notna()]["Fare"].mean()
without_cabin = data[data["Cabin"].isna()]["Fare"].mean()
fare_ratio = with_cabin / without_cabin if without_cabin != 0 else float("inf")

print("The average ticket price for passengers with a cabin:", with_cabin)
print("The average ticket price for passengers without a cabin:", without_cabin)
print("How many times do the prices differ:", fare_ratio)

sns.countplot(x="Pclass", data=data)
plt.title("The distribution of passengers by class")
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data, x="Age", y="Fare", hue="Pclass", size="Relatives", sizes=(20, 200)
)
plt.title("Fare vs. Age by Class")
plt.xlabel("Age")
plt.ylabel("Fare")
plt.show()


age_survival = data.groupby(["Age", "Survived"]).size().unstack().fillna(0)
age_survival.plot(figsize=(10, 6), title="Survived and Deceased by Age")
plt.xlabel("Age")
plt.ylabel("Number of Passengers")
plt.legend(["Deceased", "Survived"])
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(data=data, x="Age", bins=30, kde=True)
plt.title("Age Distribution of Passengers")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(data=data, x="Pclass")
plt.title("Passenger Count by Class")
plt.xlabel("Class")
plt.ylabel("Number of Passengers")
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(data=data, y="Sex", palette="pastel")
plt.title("Passenger Distribution by Gender")
plt.xlabel("Number of Passengers")
plt.ylabel("Gender")
plt.show()

survival_counts = data["Survived"].value_counts()
fig = px.pie(
    names=survival_counts.index,
    values=survival_counts.values,
    title="Survival Rate of Passengers",
)
fig.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x="Pclass", y="Fare")
plt.title("Fare by Class")
plt.xlabel("Class")
plt.ylabel("Fare")
plt.show()

fig = px.sunburst(
    data,
    path=["Pclass", "Sex"],
    values="Fare",
    title="Passenger Distribution by Class and Gender",
)
fig.show()

data["Fare"] = data["Fare"].fillna(0)

fig = px.scatter_3d(
    data,
    x="Age",
    y="Relatives",
    z="Fare",
    color="Pclass",
    size="Fare",
    title="3D Scatter Plot of Age, Relatives, and Fare",
)
fig.show()

fig = px.scatter(
    data,
    x="Age",
    y="Fare",
    color="Survived",
    symbol="Sex",
    size="Fare",
    title="Fare vs. Age with Survival Status",
)
fig.show()
