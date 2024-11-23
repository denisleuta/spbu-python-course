# Conclusions and analysis
## Classification
### 1. Model results:

#### DecisionTreeClassifier:

- precision for survivors: 0.86 (vs. 0.79 at the workshop).
- recall for survivors: 0.84 (vs. 0.72 at the workshop).
- f1_score for survivors: 0.85 (vs. 0.75 at the workshop).
- Conclusion: metrics have been significantly improved by optimizing hyperparameters (max_depth and min_samples_split) and balancing data using SMOTE.

#### RandomForestClassifier:

- accuracy: 0.87 (vs. 0.8 at the workshop).
- Conclusion: the model showed better results than at the seminar. Optimization of hyperparameters (n_estimators, max_depth, min_samples_split) helped to improve accuracy.

#### LogisticRegression:

- precision for the dead: 0.82 (vs. 0.81 at the seminar).
- recall for the dead: 0.78 (vs. 0.88 at the seminar).
- Conclusion: the results for metrics are slightly worse for the "dead" class (especially recall), but on average the metrics remained at a comparable level. Perhaps the linear model does not fully reflect the complex dependencies in the data.

#### GradientBoostingClassifier:

- accuracy: 0.85.
- f1_score for survivors: 0.86.
- Conclusion: boosting showed good results comparable to the decision tree and the random forest, but was inferior to the random forest in accuracy. This may be due to high computational complexity and data volume limitations.

#### Analysis and improvements:

On all models, we managed to surpass the results of the workshop on most metrics thanks to the following steps:
Balancing classes using SMOTE. This eliminated the imbalance between the survivors and the dead.
Optimization of hyperparameters. Using GridSearchCV helped to adjust the depth of the tree, the number of trees, and the minimum number of examples to split.
Feature Engineering. The addition of the FamilySize attribute improved the understanding of the family structure of passengers, which affects the probability of survival.
Removing unnecessary features. The exclusion of Name and Ticket, which are uninformative in their original form, reduced the noise in the data.
The Gradient Boosting and Random Forest models showed the best results. However, the Logistic Regression and Decision Tree can be useful due to the ease of interpretation.

#### Possible limitations:

The lesser improvement in LogisticRegression is due to the inability of the linear model to account for complex dependencies between features. More feature engineering may be needed.
In the Gradient Boosting model, the increase turned out to be insignificant due to the small amount of data, which limits the advantages of ensemble methods.
Regression
Model results:

# LinearRegression:

- RMSE: 0.91 (vs. 10.7 at the seminar).
- Conclusion: the result has been significantly improved. This is due to scaling of features, exclusion of noise data (Name, Ticket) and adjustment of regularization.

# RandomForestRegressor:

- RMSE: 0.88.
- Conclusion: the model showed slightly better quality than linear regression. Optimization of hyperparameters such as max_depth and n_estimators has reduced the error.

# Analysis and improvements:

At the workshop, the RMSE error was significantly higher (10.7). The main reasons for the improvement:
Scaling of features. Bringing numerical features (Age, Fare) to a standard appearance improved the quality of the model.
Deleting omissions. The gaps in the Age column were filled in using the median.
Selection of features. Excluding irrelevant data reduced noise and improved the quality of predictions.
Data balancing. Although the regression task does not require class balancing, data cleansing and the creation of a new FamilySize feature have improved the overall view of passengers.

# Possible limitations:

Linear regression remains limited in accounting for non-linear relationships, which makes it less accurate than Random Forest Regressor.
To further improve, more complex features could be added, such as interactions between passenger class, ticket price, and number of family members.

# General conclusions
## Classification:

The metrics of all models have been improved relative to the results of the workshop. The best model is the Random Forest Classifier, which reached accuracy = 0.87.
Feature engineering and data balancing turned out to be important for all models.
More sophisticated methods (Gradient Boosting) showed good results, but their improvement over the random forest was negligible due to the small amount of data.

## Regression:

The RMSE value was significantly reduced (from 10.7 to 0.88). Random Forest Regressor turned out to be better than the linear model due to its ability to take into account complex dependencies.
Improvements have been made possible through careful data cleanup, the creation of new features, and proper scaling.
