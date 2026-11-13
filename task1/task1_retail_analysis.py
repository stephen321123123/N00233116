"""Task 1: Retail performance analytics (condensed version)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data' / 'Retail_outlets.csv'
OUT = BASE / 'outputs'
OUT.mkdir(exist_ok=True)


def show(title, value):
    """Print a labelled table or result for terminal screenshots."""
    print(f'\n{title}')
    print(value.to_string() if isinstance(value, (pd.DataFrame, pd.Series)) else value)


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=150)
    plt.close()
    print(f'Saved {filename}')


# SECTION 1 - DATA INSPECTION, CLEANING AND FEATURE ENGINEERING
print('\nSECTION 1 - DATA PREPARATION')
df = pd.read_csv(DATA)
show('FIRST FIVE ROWS:', df.head())
show('DATASET SIZE:', df.shape)
show('COLUMN NAMES:', df.columns.tolist())
show('DATA TYPES:', df.dtypes)
show('MISSING VALUES:', df.isna().sum())
show('DUPLICATE ROWS:', df.duplicated().sum())
show('SUMMARY STATISTICS:', df.describe())

df = df.drop_duplicates().copy()
show('AFTER REMOVING DUPLICATES:', f'{len(df)} rows; {df.duplicated().sum()} duplicates')
show('MISSING VALUE PERCENTAGES:', (df.isna().mean() * 100).round(2))

missing_columns = ['MarketingSpend', 'OnlineTraffic', 'CustomerSatisfaction',
                   'InventoryAvailability']
for col in missing_columns:
    median = df[col].median()
    df[col] = df[col].fillna(median)
    print(f'{col}: filled missing values with median {median:.2f}')
show('MISSING VALUES AFTER CLEANING:', df.isna().sum())
show('DATASET SIZE AFTER CLEANING:', df.shape)

print('\nOUTLIER INVESTIGATION (IQR METHOD):')
for col in ['MarketingSpend', 'Footfall', 'OnlineTraffic', 'StaffHours', 'SalesRevenue']:
    q1, q3 = df[col].quantile([0.25, 0.75])
    low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    count = ((df[col] < low) | (df[col] > high)).sum()
    print(f'{col}: lower={low:.2f}, upper={high:.2f}, outliers={count}')

df['RevenuePerVisitor'] = df['SalesRevenue'] / df['Footfall'].replace(0, np.nan)
df['MarketingEfficiency'] = df['SalesRevenue'] / df['MarketingSpend'].replace(0, np.nan)
df['SalesGrowthPercent'] = (df['SalesRevenue'] - df['PreviousMonthSales']) / df['PreviousMonthSales'].replace(0, np.nan) * 100
engineered = ['RevenuePerVisitor', 'MarketingEfficiency', 'SalesGrowthPercent']
show('FEATURE ENGINEERING RESULTS:', df[engineered].head(10).round(2))
show('DATASET SIZE AFTER FEATURE ENGINEERING:', df.shape)
show('MISSING VALUES IN NEW FEATURES:', df[engineered].isna().sum())
df.to_csv(OUT / 'Retail_outlets_cleaned.csv', index=False)
print('Cleaned dataset saved successfully.')


# SECTION 2 - EXPLORATORY DATA ANALYSIS
print('\nSECTION 2 - EXPLORATORY DATA ANALYSIS')
region_analysis = df.groupby('Region').agg(
    TotalRevenue=('SalesRevenue', 'sum'), AverageRevenue=('SalesRevenue', 'mean'),
    RecordCount=('StoreID', 'count')).round(2)
store_analysis = df.groupby('StoreType').agg(
    TotalRevenue=('SalesRevenue', 'sum'), AverageRevenue=('SalesRevenue', 'mean')).round(2)
season_analysis = df.groupby('Season').agg(
    TotalRevenue=('SalesRevenue', 'sum'), AverageRevenue=('SalesRevenue', 'mean')).round(2)
marketing_analysis = df.groupby('Region').agg(
    AverageMarketingSpend=('MarketingSpend', 'mean'),
    AverageRevenue=('SalesRevenue', 'mean'),
    AverageMarketingEfficiency=('MarketingEfficiency', 'mean')).round(2)
top_stores = df.groupby('StoreID').agg(
    TotalRevenue=('SalesRevenue', 'sum'), AverageRevenue=('SalesRevenue', 'mean'),
    RecordCount=('SalesRevenue', 'count')).sort_values('TotalRevenue', ascending=False).head(5)
for title, table, sort_col in [
    ('1. REVENUE BY REGION', region_analysis, 'TotalRevenue'),
    ('2. REVENUE BY STORE TYPE', store_analysis, 'TotalRevenue'),
    ('3. REVENUE BY SEASON', season_analysis, 'TotalRevenue'),
    ('4. MARKETING PERFORMANCE BY REGION', marketing_analysis, 'AverageMarketingEfficiency')]:
    show(title, table.sort_values(sort_col, ascending=False))
show('TOP 5 STORES BY TOTAL REVENUE:', top_stores.round(2))


# SECTION 3 - PIVOT TABLES AND CORRELATION
print('\nSECTION 3 - PIVOT TABLES & CORRELATION ANALYSIS')
pivot1 = pd.pivot_table(df, values='SalesRevenue', index='Region',
                        columns='StoreType', aggfunc='mean').round(2)
pivot2 = pd.pivot_table(df, values='SalesRevenue', index='Season',
                        columns='Region', aggfunc='mean').round(2)
show('PIVOT TABLE 1 - AVERAGE REVENUE BY REGION AND STORE TYPE:', pivot1)
show('PIVOT TABLE 2 - AVERAGE REVENUE BY SEASON AND REGION:', pivot2)

numeric_columns = ['MarketingSpend', 'Footfall', 'OnlineTraffic', 'StaffHours',
                   'DiscountRate', 'CustomerSatisfaction', 'InventoryAvailability',
                   'CompetitorDistance', 'PreviousMonthSales', 'SalesRevenue']
correlation_matrix = df[numeric_columns].corr()
show('CORRELATION MATRIX:', correlation_matrix.round(2))
show('CORRELATION WITH SALES REVENUE:',
     correlation_matrix['SalesRevenue'].drop('SalesRevenue').sort_values(key=abs, ascending=False).round(3))
plt.figure(figsize=(10, 7))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap - Retail Performance')
save_chart('correlation_heatmap.png')


# SECTION 4 - PREDICTIVE ANALYTICS
print('\nSECTION 4 - PREDICTIVE ANALYTICS')
features = ['Region', 'StoreType', 'Season', 'MarketingSpend', 'Footfall',
            'OnlineTraffic', 'StaffHours', 'DiscountRate', 'CustomerSatisfaction',
            'InventoryAvailability', 'CompetitorDistance', 'PreviousMonthSales']
categorical = ['Region', 'StoreType', 'Season']
numerical = [col for col in features if col not in categorical]
X_train, X_test, y_train, y_test = train_test_split(
    df[features], df['SalesRevenue'], test_size=0.20, random_state=42)
print(f'Training rows: {len(X_train)}; Testing rows: {len(X_test)}')

preprocessor = ColumnTransformer([
    ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                      ('scaler', StandardScaler())]), numerical),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
])
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
}
results = []
trained = {}
for name, model in models.items():
    print(f'\nTRAINING MODEL: {name}', flush=True)
    pipeline = Pipeline([('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train, y_train)
    trained[name] = pipeline
    predicted = pipeline.predict(X_test)
    metrics = {'Model': name, 'MAE': mean_absolute_error(y_test, predicted),
               'RMSE': np.sqrt(mean_squared_error(y_test, predicted)),
               'R2': r2_score(y_test, predicted)}
    results.append(metrics)
    print(f"MAE: {metrics['MAE']:.2f}; RMSE: {metrics['RMSE']:.2f}; R2: {metrics['R2']:.4f}")
results_df = pd.DataFrame(results)
show('MODEL COMPARISON:', results_df.round(3))
results_df.to_csv(OUT / 'model_comparison.csv', index=False)


# SECTION 5 - FEATURE IMPORTANCE
print('\nSECTION 5 - FEATURE IMPORTANCE ANALYSIS')
# Reuse the already-trained Random Forest instead of fitting it a second time.
rf_pipeline = trained['Random Forest']
feature_names = rf_pipeline.named_steps['preprocessor'].get_feature_names_out()
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf_pipeline.named_steps['model'].feature_importances_
})
importance_df['Feature'] = (importance_df['Feature']
                            .str.replace('num__', '', regex=False)
                            .str.replace('cat__', '', regex=False))
importance_df = importance_df.sort_values('Importance', ascending=False)
top_features = importance_df.head(10)
show('FEATURE IMPORTANCE RANKING:', importance_df.round(4))
show('TOP 10 MOST IMPORTANT FEATURES:', top_features.round(4))
importance_df.to_csv(OUT / 'feature_importance.csv', index=False)
plt.figure(figsize=(11, 7))
plt.barh(top_features['Feature'][::-1], top_features['Importance'][::-1])
plt.xlabel('Feature Importance Score')
plt.ylabel('Feature')
plt.title('Top 10 Features Influencing Sales Revenue Predictions')
save_chart('feature_importance.png')


# SECTION 6 - DATA VISUALISATION
print('\nSECTION 6 - DATA VISUALISATION')
sns.set_theme(style='whitegrid')
chart_specs = [
    ('revenue_by_region.png', 'Total Sales Revenue by Region', 'Region',
     'Total Sales Revenue', region_analysis['TotalRevenue'].sort_values(ascending=False), 'steelblue'),
    ('revenue_by_season.png', 'Average Sales Revenue by Season', 'Season',
     'Average Sales Revenue', season_analysis['AverageRevenue'].reindex(
         ['Spring', 'Summer', 'Autumn', 'Winter']), 'seagreen'),
    ('marketing_efficiency_by_region.png', 'Average Marketing Efficiency by Region',
     'Region', 'Sales Revenue / Marketing Spend',
     marketing_analysis['AverageMarketingEfficiency'].sort_values(ascending=False), 'mediumpurple')
]
for filename, title, xlabel, ylabel, values, color in chart_specs:
    plt.figure(figsize=(9, 6))
    sns.barplot(x=values.index, y=values.values, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    save_chart(filename)
print('\nAll Section 6 charts saved successfully.')