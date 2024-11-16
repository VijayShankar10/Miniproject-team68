# -*- coding: utf-8 -*-
"""spendgenius.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wAd_SDViR2xkacp2MTAjOLSeIqE1sMH7
"""

!pip install ydata-profiling # Install the ydata-profiling package
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ydata_profiling import ProfileReport # Now this import should work
import warnings as w
w.filterwarnings('ignore')

df = pd.read_csv('/content/data.csv')
df.head()

df.info()

df.isnull().sum()

df.duplicated().sum()

statistics = df.describe().transpose()
statistics['CV'] = statistics['std'] / statistics['mean'] * 100 # this is the coefficient variation  which help us to identify std is high or low ........
statistics.astype(int)

df.describe(include='object')

numeric = df.select_dtypes(include = ['int' , 'float']).columns

fig = px.box(df,
             y=numeric,
             title="Box Plots of Numerical Features",
             labels={col: col for col in numeric},
            height = 600)  # Set labels for the axes
fig.update_layout(xaxis_title="Numerical Features", yaxis_title="Values")
fig.show()

!pip install ydata-profiling --upgrade # Update ydata-profiling to the latest version.

import pandas as pd
from ydata_profiling import ProfileReport
report = ProfileReport(df, title = ' EDA REPROT FOR THE DATA ')
report

def age_bracket(age):
    if 18 < age <=30:
        return '20s'
    elif 30 < age <=40:
        return '30s'
    elif 40<age<=50:
        return '40s'
    elif 50<age<=60:
        return '50s'
    else:
        return '60s'
df['age_bracket'] = df['Age'].apply(age_bracket)

avg_income_age = df.groupby('age_bracket')['Income'].mean().reset_index().sort_values(by = 'Income' , ascending = False)
avg_income_occupation = df.groupby('Occupation')['Income'].mean().reset_index().sort_values(by = 'Income', ascending = False)
avg_income_city = df.groupby('City_Tier')['Income'].mean().reset_index().sort_values(by = 'Income', ascending = False)

fig  = px.bar(avg_income_age , x= 'age_bracket', y = 'Income' , color = 'age_bracket' , title = 'AVG INCOME BY AGE GROPUS ')
fig.show()
fig  = px.bar(avg_income_occupation , x= 'Occupation', y = 'Income' , color = 'Occupation' , title = 'AVG INCOME BY OCCUPATION ')
fig.show()
fig  = px.bar(avg_income_city , x= 'City_Tier', y = 'Income' , color = 'City_Tier' , title = 'AVG INCOME BY CITY TIER ')
fig.show()

variable = 'Dependents'
correlation  = df.corr( numeric_only= True )[variable]
correlation_df = correlation.reset_index()
correlation_df.columns = ['Variable', 'Correlation']
fig = px.bar(correlation_df , x = 'Variable' , y = 'Correlation' , labels={'Correlation': 'Correlation Coefficient'},
             color='Correlation', title = 'CORRELATION OF DEPENDENTS BETWEEN OTHER VARIABLES')
fig.show()

def income_bracket(income):
    if 1000  < income <=30000:
        return 'Lower Class'
    elif 30000 < income <=100000:
        return 'MIddle Class'
    else:
        return 'High Class'
df['income_bracket'] = df['Income'].apply(income_bracket)

expense_df  = df[['Rent',
       'Loan_Repayment', 'Insurance', 'Groceries', 'Transport', 'Eating_Out',
       'Entertainment', 'Utilities', 'Healthcare', 'Education',
       'Miscellaneous' , 'age_bracket', 'income_bracket' , 'City_Tier']]

group = expense_df.groupby(['age_bracket' , 'income_bracket', 'City_Tier'])[['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 'Transport',
       'Eating_Out', 'Entertainment', 'Utilities', 'Healthcare', 'Education',
       'Miscellaneous']].mean().reset_index().sort_values(by = ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 'Transport',
       'Eating_Out', 'Entertainment', 'Utilities', 'Healthcare', 'Education',
       'Miscellaneous'] , ascending  = False)

# Reshape the DataFrame for visualization

melted_group = group.melt(id_vars=['age_bracket', 'income_bracket', 'City_Tier'],
                           var_name='Expense Category',
                           value_name='Average Expense')
melted_group = melted_group.sort_values(by='Average Expense', ascending=False)

# Create the bar plot

fig = px.bar(melted_group,
             x='Expense Category',
             y='Average Expense',
             color='age_bracket',
             barmode='group',
             facet_row='income_bracket',
             facet_col='City_Tier',
             title='Average Expenses by Demographics',
             labels={'Average Expense': 'Average Expense (₹)',
                     'Expense Category': 'Expense Category'}, height = 850)

# Update layout for black background

fig.update_layout(
    plot_bgcolor='white',  # Background color for the plot area
    paper_bgcolor='blue',  # Background color for the entire figure
    font_color='white'      # Font color for titles, labels, and legends
)
# Show the plot
fig.show()

expense_df['Income'] = df['Income']

essential_expense = ['Rent', 'Loan_Repayment', 'Groceries', 'Utilities', 'Healthcare', 'Education']
discreationary = ['Insurance' , 'Transport' , 'Eating_Out' , 'Entertainment' , 'Miscellaneous']

# Calculate total essential and discretionary expenses for each income bracket
expense_df['Total_Essential_Expense'] = expense_df[essential_expense].sum(axis=1)
expense_df['Total_Discretionary_Expense'] = expense_df[discreationary].sum(axis=1)

# Calculate the proportion of income spent on essentials and discretionary expenses

expense_df['Proportion_Essential'] = expense_df['Total_Essential_Expense'] / expense_df['Income']
expense_df['Proportion_Discretionary'] = expense_df['Total_Discretionary_Expense'] / expense_df['Income']

total_proportion  = ['Proportion_Essential', 'Proportion_Discretionary']
avg_proportion = expense_df.groupby('income_bracket')[total_proportion].mean().reset_index()
avg_proportion

# Create subplots
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]], subplot_titles=('Essential Expenses Proportion', 'Discretionary Expenses Proportion'))

# Add the pie chart for Essential Expenses

fig.add_trace(
    go.Pie(labels=avg_proportion['income_bracket'],
           values=avg_proportion['Proportion_Essential'],
           name="Essential Expenses",
           marker=dict(colors=px.colors.qualitative.Plotly)),
    row=1, col=1
)

# Add the pie chart for Discretionary Expenses
fig.add_trace(
    go.Pie(labels=avg_proportion['income_bracket'],
           values=avg_proportion['Proportion_Discretionary'],
           name="Discretionary Expenses",
           marker=dict(colors=px.colors.qualitative.Plotly)),
    row=1, col=2
)

# Update layout

fig.update_layout(title_text='Proportion of Expenses by Income Bracket',
                  paper_bgcolor='brown',  # Background color for the entire figure
                  font_color='white',
                  height=400)
# Show the figure
fig.show()

"""**Financial Goals &** **Savings**"""

# creating a new column to calculate the Disposable_Income_Percentage.............
df['Disposable_Income_Percentage'] = df['Disposable_Income'] / df['Income'] * 100

df[['Income' , 'Disposable_Income' , 'Desired_Savings' , 'Desired_Savings_Percentage' , 'Disposable_Income_Percentage']].astype(int)

# now we are calculating the savings diffrence in order to find out those people who are actually save their income or those who are not saving thier income according to thier desire......

df['savings_diffrence'] = df['Disposable_Income_Percentage'] - df['Desired_Savings_Percentage']
df['savings_status'] = df['savings_diffrence'].apply(lambda x : 'success' if x >= 0  else 'failed') # here we have labeled the positive savings as ( success ) and negative savings as ( failed )
df[['Income' , 'Disposable_Income' , 'Desired_Savings' , 'Desired_Savings_Percentage' , 'Disposable_Income_Percentage' , 'savings_diffrence' , 'savings_status']]

# # Step 3: Filter Individuals Below Target
negative_savings = df[df['savings_status'] == 'failed' ]

# Step 4: Calculate Total Expenses
# Define expense columns to sum up for total expenses
expense_columns = ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 'Transport', 'Eating_Out',
                   'Entertainment', 'Utilities', 'Healthcare', 'Education', 'Miscellaneous']
negative_savings['total_expense'] = negative_savings[expense_columns].sum(axis=1)

# Step 5: Calculate Contribution of Each Category to Total Expenses
# For each expense column, calculate the percentage of Total_Expenses
for col in expense_columns:
    negative_savings[f'{col}_contribution'] = (negative_savings[col] / negative_savings['total_expense']) * 100

# Step 6: Aggregate Insights - Average Contribution of Each Category for Individuals Below Target
# Calculate the mean contribution of each category
avg_contribution = negative_savings[[f'{col}_contribution' for col in expense_columns]].mean()

fig = px.pie(avg_contribution , names = avg_contribution.index , values = avg_contribution.values , title = "EXPENSE CATEGORIES CONTRIBUTION IN PEOPLE'S NEGATIVE SPENDINGS" )

fig.update_layout(
    paper_bgcolor = 'black',
    font_color = 'white')

fig.show()

"""**desired savings percentage vary across different demographic profiles**"""

savings_group = df.groupby(['age_bracket' , 'income_bracket' , 'Occupation' ,
                            'City_Tier'])['Desired_Savings_Percentage'].mean().reset_index().sort_values(
                             by = 'Desired_Savings_Percentage' , ascending  = False )
savings_group

# Create the bar plot

fig = px.bar(savings_group,
             x='Occupation',
             y='Desired_Savings_Percentage',
             color='age_bracket',
             barmode='group',
             facet_row='income_bracket',
             facet_col='City_Tier',
             title='Average Desired Savings Percentage by Demographics',
             height = 850)

# Update layout for black background
fig.update_layout(
    plot_bgcolor='black',  # Background color for the plot area
    paper_bgcolor='black',  # Background color for the entire figure
    font_color='white'      # Font color for titles, labels, and legends
)

# Show the plot
fig.show()

"""**Disposable Income**"""

corr = df.corr(numeric_only=True)['Disposable_Income']
fig = px.bar(corr , color = 'value' , height = 600  , labels={'index' : 'columns' , 'value' : 'correlation values'} ,
            title = 'Disposable Income Correlation with other variables ')
fig.update_layout(
    paper_bgcolor = 'black',
    plot_bgcolor = 'black' ,
    font_color = 'white')
fig.show()

"""**Potential Savings Analysis**

"""

# Define columns for potential savings

potential_savings_columns = [
    'Potential_Savings_Groceries', 'Potential_Savings_Transport',
    'Potential_Savings_Eating_Out', 'Potential_Savings_Entertainment',
    'Potential_Savings_Utilities', 'Potential_Savings_Healthcare',
    'Potential_Savings_Education', 'Potential_Savings_Miscellaneous'
]

# Step 1: Summarize Potential Savings by Category
# Calculate the average potential savings for each category
avg_potential_savings = df[potential_savings_columns].mean().sort_values(ascending=False)
print("Average Potential Savings by Category:\n", avg_potential_savings)

# Step 2: Calculate the Impact on Disposable Income if Savings are Realized
# Calculate total potential savings per individual
df['Total_Potential_Savings'] = df[potential_savings_columns].sum(axis=1)

# Calculate new disposable income if potential savings are realized
df['Disposable_Income_Realized'] = df['Disposable_Income'] + df['Total_Potential_Savings']
# Calculate the change in disposable income from realizing savings
df['Disposable_Income_Change_Percentage'] = (
    (df['Disposable_Income_Realized'] - df['Disposable_Income']) / df['Disposable_Income']
) * 100

# Step 3: Summarize Impact by Showing Average Change in Disposable Income
avg_disposable_income_change = df['Disposable_Income_Change_Percentage'].mean()
print(f"\nAverage Change in Disposable Income if Potential Savings are Realized: {avg_disposable_income_change:.2f}%")

# Optional: Show impact by category
category_impact = (avg_potential_savings / df['Disposable_Income'].mean()) * 100
print("\nImpact of Each Category's Potential Savings on Disposable Income (as % of avg disposable income):\n", category_impact)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Load and preprocess the data
data = pd.read_csv('/content/data.csv')
X = data[['Disposable_Income', 'Desired_Savings_Percentage']]
y = data['Income']  # Replace with your spending target column

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Train and evaluate each model
for model_name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"{model_name} MSE: {mse:.2f}")

# Select the best model (example using Gradient Boosting) for final predictions
best_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
best_model.fit(X_train, y_train)
new_data = pd.DataFrame({'Disposable_Income': [5000], 'Desired_Savings_Percentage': [20]})
new_data = scaler.transform(new_data)
prediction = best_model.predict(new_data)
print(f"Predicted Spending: {prediction[0]:.2f}")

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Evaluate models and print results
for model_name, model in models.items():
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"{model_name} Evaluation Metrics:")
    print(f" - Mean Absolute Error (MAE): {mae:.2f}")
    print(f" - Mean Squared Error (MSE): {mse:.2f}")
    print(f" - R-squared (R²): {r2:.2f}\n")

"""# **Plot Predicted vs. Actual Spending**"""

import matplotlib.pyplot as plt

# Predictions using the best model (Gradient Boosting)
predictions = best_model.predict(X_test)

# Plot Predicted vs Actual
plt.figure(figsize=(10, 6))
plt.scatter(y_test, predictions, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', color='red', lw=2)
plt.xlabel('Actual Spending')
plt.ylabel('Predicted Spending')
plt.title('Predicted vs Actual Spending')
plt.show()

"""# **Residual Plot**"""

# Calculate residuals
residuals = y_test - predictions

# Plot residuals
plt.figure(figsize=(10, 6))
plt.scatter(predictions, residuals, color='purple')
plt.hlines(y=0, xmin=predictions.min(), xmax=predictions.max(), color='red', linestyle='--')
plt.xlabel('Predicted Spending')
plt.ylabel('Residuals')
plt.title('Residuals Plot')
plt.show()

"""# **Best model for the prediction**"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Gradient Boosting Performance Summary:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R²): {r2:.2f}")

"""# **feature importance analysis**"""

importances = best_model.feature_importances_
features = X.columns
plt.figure(figsize=(10, 6))
plt.barh(features, importances, color='skyblue')
plt.xlabel("Feature Importance")
plt.title("Feature Importance in Gradient Boosting Model")
plt.show()

"""# **Cross-Validation**"""

from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='r2')
print("Cross-Validation R² Scores:", cv_scores)
print("Average Cross-Validation R² Score:", cv_scores.mean())

"""# **Hyperparameter Tuning**"""

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search = GridSearchCV(estimator=best_model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")

import joblib

# Save the model
joblib.dump(grid_search.best_estimator_, 'spending_prediction_model.pkl')

# Load the saved model
loaded_model = joblib.load('spending_prediction_model.pkl')