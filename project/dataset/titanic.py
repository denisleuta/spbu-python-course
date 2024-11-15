import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import warnings


# Load data from CSV files
train = pd.read_csv("project/dataset/train.csv")
test = pd.read_csv("project/dataset/test.csv")

# Combine training and test datasets into a single DataFrame
data = pd.concat([train, test], ignore_index=True)

# Convert relevant columns to categorical type for better analysis
data["Survived"] = data["Survived"].astype("category")
data["Pclass"] = data["Pclass"].astype("category")
data["Sex"] = data["Sex"].astype("category")

# Print descriptive statistics of the combined dataset
print(data.describe())

# Count the number of passengers in each class
print(data["Pclass"].value_counts())

# Calculate the average age of passengers grouped by class and sex
age_stats = data.groupby(["Pclass", "Sex"])["Age"].mean()
print(age_stats)

# Identify the youngest and oldest passengers based on class and sex
youngest = age_stats.idxmin(), age_stats.min()
oldest = age_stats.idxmax(), age_stats.max()
print("The Youngest:", youngest)
print("The Oldest:", oldest)

# Filter survivors whose names start with 'K'
survivors_with_k = data[(data["Survived"] == 1) & (data["Name"].str.startswith("K"))]
# Sort by fare in descending order
survivors_with_k_sorted = survivors_with_k.sort_values(by="Fare", ascending=False)

# Print the names of the highest and lowest fare-paying survivors with 'K'
print("Passenger paid more than all:", survivors_with_k_sorted.iloc[0]["Name"])
print("Passenger paid less than all:", survivors_with_k_sorted.iloc[-1]["Name"])
print(survivors_with_k_sorted)

# Create a new column that sums the number of relatives (SibSp + Parch)
data["Relatives"] = data["SibSp"] + data["Parch"]
# Find the maximum number of relatives among survivors
max_relatives = data[data["Survived"] == 1]["Relatives"].max()
print("Max relatives:", max_relatives)

# Calculate average fare for passengers with and without cabins
with_cabin = data[data["Cabin"].notna()]["Fare"].mean()
without_cabin = data[data["Cabin"].isna()]["Fare"].mean()
fare_ratio = with_cabin / without_cabin if without_cabin != 0 else float("inf")

# Print average fare for both groups
print("The average ticket price for passengers with a cabin:", with_cabin)
print("The average ticket price for passengers without a cabin:", without_cabin)
print("How many times do the prices differ:", fare_ratio)

# Visualize the distribution of passengers by class using countplot
sns.countplot(x="Pclass", data=data)
plt.title("The distribution of passengers by class")
plt.show()

# Group by columns and count the number
grouped_data = data.groupby(["Pclass", "Sex", "Survived"]).size()

# Convert Series to DataFrame directly
sankey_data = pd.DataFrame(grouped_data).reset_index()
sankey_data = pd.DataFrame(grouped_data, columns=["Count"]).reset_index()

# Define unique classes, sexes, and survival statuses
classes = sorted(data["Pclass"].unique())
sexes = sorted(data["Sex"].unique())
survival_status = ["Did not Survive", "Survived"]

# Create nodes for the Sankey diagram
nodes = {
    **{f"Class {cls}": i for i, cls in enumerate(classes)},
    **{sex: i + len(classes) for i, sex in enumerate(sexes)},
    **{
        status: i + len(classes) + len(sexes)
        for i, status in enumerate(survival_status)
    },
}

sources = []
targets = []
values = []

# Fill sources, targets, and values lists for the Sankey diagram
for cls in classes:
    for sex in sexes:
        count = sankey_data[
            (sankey_data["Pclass"] == cls) & (sankey_data["Sex"] == sex)
        ]["Count"].sum()

        if count > 0:
            sources.append(nodes[f"Class {cls}"])
            targets.append(nodes[sex])
            values.append(count)

for sex in sexes:
    for i, status in enumerate([0, 1]):
        count = sankey_data[
            (sankey_data["Sex"] == sex) & (sankey_data["Survived"] == status)
        ]["Count"].sum()
        if count > 0:
            sources.append(nodes[sex])
            targets.append(nodes[survival_status[status]])
            values.append(count)

# Create Sankey diagram using Plotly
fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=list(nodes.keys()),
        ),
        link=dict(source=sources, target=targets, value=values),
    )
)

fig.update_layout(title_text="Passenger Flow by Class, Sex, and Survival", font_size=12)
fig.show()

# Visualize the relationship between age and fare considering class and number of relatives
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data, x="Age", y="Fare", hue="Pclass", size="Relatives", sizes=(20, 200)
)
plt.title("Fare vs. Age by Class")
plt.xlabel("Age")
plt.ylabel("Fare")
plt.show()

# Analyze survival based on age
age_survival = data.groupby(["Age", "Survived"]).size().unstack().fillna(0)
age_survival.plot(figsize=(10, 6), title="Survived and Deceased by Age")
plt.xlabel("Age")
plt.ylabel("Number of Passengers")
plt.legend(["Deceased", "Survived"])
plt.show()

# Visualize age distribution of passengers using a histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=data, x="Age", bins=30, kde=True)
plt.title("Age Distribution of Passengers")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Visualize passenger count by class using countplot
plt.figure(figsize=(8, 6))
sns.countplot(data=data, x="Pclass")
plt.title("Passenger Count by Class")
plt.xlabel("Class")
plt.ylabel("Number of Passengers")
plt.show()

# Visualize passenger distribution by gender using countplot
plt.figure(figsize=(8, 6))
sns.countplot(data=data, y="Sex", palette="pastel")
plt.title("Passenger Distribution by Gender")
plt.xlabel("Number of Passengers")
plt.ylabel("Gender")
plt.show()

# Visualize survival rates with a pie chart
survival_counts = data["Survived"].value_counts()
fig = px.pie(
    names=survival_counts.index,
    values=survival_counts.values,
    title="Survival Rate of Passengers",
)
fig.show()

# Visualize fare by class using boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x="Pclass", y="Fare")
plt.title("Fare by Class")
plt.xlabel("Class")
plt.ylabel("Fare")
plt.show()

# Suppress FutureWarnings for cleaner output
warnings.simplefilter(action="ignore", category=FutureWarning)

# Visualize passenger distribution by class and gender using a sunburst chart
fig = px.sunburst(
    data,
    path=["Pclass", "Sex"],
    values="Fare",
    title="Passenger Distribution by Class and Gender",
)
fig.show()

# Replace missing values in 'Fare' column with 0 for further analysis
data["Fare"] = data["Fare"].fillna(0)

# Visualize a 3D scatter plot to analyze relationships between age, relatives, and fare
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

# Visualize the relationship between age and fare considering survival status and gender
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
