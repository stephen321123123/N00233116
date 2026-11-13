# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent
# DATA_DIR = BASE_DIR / "data"
# OUTPUT_DIR = BASE_DIR / "outputs"

# OUTPUT_DIR.mkdir(exist_ok=True)

# import pandas as pd

# # Load the retail dataset

# df = pd.read_csv(DATA_DIR / "Retail_outlets.csv")

# # Display the first five rows
# print("\nFIRST FIVE ROWS:")
# print(df.head().to_string())

# # Display dataset dimensions
# print("\nDATASET SIZE:")
# print(df.shape)

# # Display column names
# print("\nCOLUMN NAMES:")
# print(df.columns.tolist())

# # Check data types
# print("\nDATA TYPES:")
# print(df.dtypes)

# # Check missing values
# print("\nMISSING VALUES:")
# print(df.isnull().sum())

# # Check duplicate rows
# print("\nDUPLICATE ROWS:")
# print(df.duplicated().sum())

# # Display summary statistics
# print("\nSUMMARY STATISTICS:")
# print(df.describe().to_string())



# # Remove duplicate rows
# df = df.drop_duplicates().copy()

# # Check the results
# print("\nAFTER REMOVING DUPLICATES:")
# print("Remaining rows:", len(df))
# print("Duplicate rows:", df.duplicated().sum())


# # -----------------------------------
# # MISSING VALUE ANALYSIS
# # -----------------------------------

# # Check missing values after removing duplicates
# print("\nMISSING VALUES AFTER DUPLICATE REMOVAL:")
# print(df.isnull().sum())

# # Calculate percentage of missing values
# print("\nMISSING VALUE PERCENTAGES:")
# print((df.isnull().mean() * 100).round(2))


# # -----------------------------------
# # HANDLE MISSING VALUES
# # -----------------------------------

# # Columns containing missing numerical values
# missing_columns = [
#     "MarketingSpend",
#     "OnlineTraffic",
#     "CustomerSatisfaction",
#     "InventoryAvailability"
# ]

# # Replace missing values with each column's median
# for column in missing_columns:
#     median_value = df[column].median()
#     df[column] = df[column].fillna(median_value)

#     print(f"{column}: filled missing values with median {median_value:.2f}")

# # Verify that missing values have been handled
# print("\nMISSING VALUES AFTER CLEANING:")
# print(df.isnull().sum())

# print("\nDATASET SIZE AFTER CLEANING:")
# print(df.shape)


# # -----------------------------------
# # OUTLIER INVESTIGATION
# # -----------------------------------

# # Select numerical columns to investigate
# outlier_columns = [
#     "MarketingSpend",
#     "Footfall",
#     "OnlineTraffic",
#     "StaffHours",
#     "SalesRevenue"
# ]

# print("\nOUTLIER INVESTIGATION (IQR METHOD):")

# for column in outlier_columns:

#     # Calculate the first and third quartiles
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)

#     # Calculate the interquartile range
#     IQR = Q3 - Q1

#     # Calculate lower and upper boundaries
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR

#     # Find values outside the boundaries
#     outliers = df[
#         (df[column] < lower_bound) |
#         (df[column] > upper_bound)
#     ]

#     print(f"\n{column}")
#     print(f"Lower bound: {lower_bound:.2f}")
#     print(f"Upper bound: {upper_bound:.2f}")
#     print(f"Number of outliers: {len(outliers)}")

    
# # -----------------------------------
# # FEATURE ENGINEERING
# # -----------------------------------

# # Feature 1: Revenue generated per visitor
# df["RevenuePerVisitor"] = (
#     df["SalesRevenue"] / df["Footfall"].replace(0, float("nan"))
# )

# # Feature 2: Revenue relative to marketing spend
# df["MarketingEfficiency"] = (
#     df["SalesRevenue"] / df["MarketingSpend"].replace(0, float("nan"))
# )

# # Feature 3: Percentage change from previous month's sales
# df["SalesGrowthPercent"] = (
#     (df["SalesRevenue"] - df["PreviousMonthSales"])
#     / df["PreviousMonthSales"].replace(0, float("nan"))
# ) * 100

# # Display the new features
# print("\nFEATURE ENGINEERING RESULTS:")

# print(df[
#     [
#         "RevenuePerVisitor",
#         "MarketingEfficiency",
#         "SalesGrowthPercent"
#     ]
# ].head(10).round(2).to_string())

# # Verify dataset dimensions
# print("\nDATASET SIZE AFTER FEATURE ENGINEERING:")
# print(df.shape)

# # Check for missing values in engineered features
# print("\nMISSING VALUES IN NEW FEATURES:")
# print(df[
#     [
#         "RevenuePerVisitor",
#         "MarketingEfficiency",
#         "SalesGrowthPercent"
#     ]
# ].isnull().sum())


# # Save cleaned dataset with engineered features

# df.to_csv(OUTPUT_DIR / "Retail_outlets_cleaned.csv", index=False)

# print("\nCleaned dataset saved successfully.")


# # ===================================
# # SECTION 2 - EXPLORATORY DATA ANALYSIS
# # ===================================

# print("\nSECTION 2 - EXPLORATORY DATA ANALYSIS")

# # GROUPBY 1 - Revenue by Region
# print("\n1. REVENUE BY REGION")

# region_analysis = df.groupby("Region").agg(
#     TotalRevenue=("SalesRevenue", "sum"),
#     AverageRevenue=("SalesRevenue", "mean"),
#     RecordCount=("StoreID", "count")
# ).round(2)

# print(region_analysis.sort_values(
#     "TotalRevenue", ascending=False
# ).to_string())


# # GROUPBY 2 - Revenue by Store Type
# print("\n2. REVENUE BY STORE TYPE")

# store_analysis = df.groupby("StoreType").agg(
#     TotalRevenue=("SalesRevenue", "sum"),
#     AverageRevenue=("SalesRevenue", "mean")
# ).round(2)

# print(store_analysis.sort_values(
#     "TotalRevenue", ascending=False
# ).to_string())


# # GROUPBY 3 - Seasonal Performance
# print("\n3. REVENUE BY SEASON")

# season_analysis = df.groupby("Season").agg(
#     TotalRevenue=("SalesRevenue", "sum"),
#     AverageRevenue=("SalesRevenue", "mean")
# ).round(2)

# print(season_analysis.sort_values(
#     "TotalRevenue", ascending=False
# ).to_string())


# # GROUPBY 4 - Marketing Performance by Region
# print("\n4. MARKETING PERFORMANCE BY REGION")

# marketing_analysis = df.groupby("Region").agg(
#     AverageMarketingSpend=("MarketingSpend", "mean"),
#     AverageRevenue=("SalesRevenue", "mean"),
#     AverageMarketingEfficiency=("MarketingEfficiency", "mean")
# ).round(2)

# print(marketing_analysis.sort_values(
#     "AverageMarketingEfficiency", ascending=False
# ).to_string())


# # TOP 5 STORES BY TOTAL REVENUE
# print("\nTOP 5 STORES BY TOTAL REVENUE")

# top_stores = df.groupby("StoreID").agg(
#     TotalRevenue=("SalesRevenue", "sum"),
#     AverageRevenue=("SalesRevenue", "mean"),
#     RecordCount=("SalesRevenue", "count")
# ).sort_values("TotalRevenue", ascending=False).head(5)

# print(top_stores.round(2).to_string())


# # ===================================
# # SECTION 3 - PIVOT TABLES & CORRELATION
# # ===================================

# print("\nSECTION 3 - PIVOT TABLES & CORRELATION ANALYSIS")

# # PIVOT TABLE 1 - Average Revenue by Region and Store Type
# print("\nPIVOT TABLE 1 - AVERAGE REVENUE BY REGION AND STORE TYPE")

# pivot1 = pd.pivot_table(
#     df,
#     values="SalesRevenue",
#     index="Region",
#     columns="StoreType",
#     aggfunc="mean"
# ).round(2)

# print(pivot1.to_string())


# # PIVOT TABLE 2 - Average Revenue by Season and Region
# print("\nPIVOT TABLE 2 - AVERAGE REVENUE BY SEASON AND REGION")

# pivot2 = pd.pivot_table(
#     df,
#     values="SalesRevenue",
#     index="Season",
#     columns="Region",
#     aggfunc="mean"
# ).round(2)

# print(pivot2.to_string())


# # CORRELATION ANALYSIS
# print("\nCORRELATION ANALYSIS")

# # Select original numerical variables
# numeric_columns = [
#     "MarketingSpend",
#     "Footfall",
#     "OnlineTraffic",
#     "StaffHours",
#     "DiscountRate",
#     "CustomerSatisfaction",
#     "InventoryAvailability",
#     "CompetitorDistance",
#     "PreviousMonthSales",
#     "SalesRevenue"
# ]

# # Calculate correlation matrix
# correlation_matrix = df[numeric_columns].corr()

# print("\nCORRELATION MATRIX:")
# print(correlation_matrix.round(2).to_string())

# # Find correlations with SalesRevenue
# print("\nCORRELATION WITH SALES REVENUE:")

# revenue_correlation = (
#     correlation_matrix["SalesRevenue"]
#     .drop("SalesRevenue")
#     .sort_values(key=abs, ascending=False)
# )

# print(revenue_correlation.round(3).to_string())


# import matplotlib
# matplotlib.use("Agg")

# import matplotlib.pyplot as plt
# import seaborn as sns

# # CREATE CORRELATION HEATMAP
# print("\nStarting heatmap generation...", flush=True)

# plt.figure(figsize=(10, 7))

# sns.heatmap(
#     correlation_matrix,
#     annot=True,
#     cmap="coolwarm",
#     fmt=".2f"
# )

# plt.title("Correlation Heatmap - Retail Performance")
# plt.tight_layout()

# print("Saving heatmap...", flush=True)


# plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
# plt.close()

# print("Correlation heatmap saved successfully.", flush=True)





# # ==========================================
# # SECTION 4 - PREDICTIVE ANALYTICS
# # ==========================================

# print("\nSECTION 4 - PREDICTIVE ANALYTICS")

# from sklearn.model_selection import train_test_split
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.impute import SimpleImputer
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# import numpy as np

# # Select features used to predict sales revenue
# # Exclude engineered features derived from SalesRevenue
# # to prevent data leakage.
# features = [
#     "Region",
#     "StoreType",
#     "Season",
#     "MarketingSpend",
#     "Footfall",
#     "OnlineTraffic",
#     "StaffHours",
#     "DiscountRate",
#     "CustomerSatisfaction",
#     "InventoryAvailability",
#     "CompetitorDistance",
#     "PreviousMonthSales"
# ]

# X = df[features]
# y = df["SalesRevenue"]

# # Split into 80% training and 20% testing
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.20, random_state=42
# )

# print("\nTRAINING AND TESTING DATA")
# print("Training rows:", len(X_train))
# print("Testing rows:", len(X_test))

# # Prepare numerical and categorical columns
# categorical_features = ["Region", "StoreType", "Season"]
# numerical_features = [
#     col for col in features if col not in categorical_features
# ]

# numeric_transformer = Pipeline([
#     ("imputer", SimpleImputer(strategy="median")),
#     ("scaler", StandardScaler())
# ])

# categorical_transformer = OneHotEncoder(
#     handle_unknown="ignore"
# )

# preprocessor = ColumnTransformer([
#     ("num", numeric_transformer, numerical_features),
#     ("cat", categorical_transformer, categorical_features)
# ])

# # Create two predictive models
# models = {
#     "Linear Regression": LinearRegression(),
#     "Random Forest": RandomForestRegressor(
#         n_estimators=100,
#         random_state=42,
#         n_jobs=-1
#     )
# }

# results = []

# for name, model in models.items():

#     print(f"\nTRAINING MODEL: {name}", flush=True)

#     pipeline = Pipeline([
#         ("preprocessor", preprocessor),
#         ("model", model)
#     ])

#     pipeline.fit(X_train, y_train)

#     predictions = pipeline.predict(X_test)

#     mae = mean_absolute_error(y_test, predictions)
#     rmse = np.sqrt(mean_squared_error(y_test, predictions))
#     r2 = r2_score(y_test, predictions)

#     results.append({
#         "Model": name,
#         "MAE": mae,
#         "RMSE": rmse,
#         "R2": r2
#     })

#     print("MAE:", round(mae, 2))
#     print("RMSE:", round(rmse, 2))
#     print("R2 Score:", round(r2, 4))

# # Compare model performance
# results_df = pd.DataFrame(results)

# print("\nMODEL COMPARISON")
# print(results_df.round(3).to_string(index=False))

# # Save model results

# results_df.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)

# print("\nModel comparison saved successfully.")




# # ==========================================
# # SECTION 5 - FEATURE IMPORTANCE
# # ==========================================

# print("\nSECTION 5 - FEATURE IMPORTANCE ANALYSIS")

# # Train Random Forest using the same training data
# # and preprocessing steps as Section 4

# rf_pipeline = Pipeline([
#     ("preprocessor", preprocessor),
#     ("model", RandomForestRegressor(
#         n_estimators=100,
#         random_state=42,
#         n_jobs=-1
#     ))
# ])

# rf_pipeline.fit(X_train, y_train)

# # Extract feature names after preprocessing
# feature_names = rf_pipeline.named_steps[
#     "preprocessor"
# ].get_feature_names_out()

# # Extract feature importance values
# importance_values = rf_pipeline.named_steps[
#     "model"
# ].feature_importances_

# # Create feature importance table
# importance_df = pd.DataFrame({
#     "Feature": feature_names,
#     "Importance": importance_values
# })

# # Remove prefixes added by ColumnTransformer
# importance_df["Feature"] = (
#     importance_df["Feature"]
#     .str.replace("num__", "", regex=False)
#     .str.replace("cat__", "", regex=False)
# )

# # Sort from most important to least important
# importance_df = importance_df.sort_values(
#     by="Importance",
#     ascending=False
# )

# print("\nFEATURE IMPORTANCE RANKING:")
# print(importance_df.round(4).to_string(index=False))

# # Display top 10 features
# top_features = importance_df.head(10)

# print("\nTOP 10 MOST IMPORTANT FEATURES:")
# print(top_features.round(4).to_string(index=False))

# # Save results
# importance_df.to_csv(
#     OUTPUT_DIR / "feature_importance.csv",
#     index=False
# )

# print("\nFeature importance saved successfully.")

# # ==========================================
# # FEATURE IMPORTANCE VISUALISATION
# # ==========================================

# print("\nGenerating feature importance chart...", flush=True)

# plt.figure(figsize=(11, 7))

# plt.barh(
#     top_features["Feature"][::-1],
#     top_features["Importance"][::-1]
# )

# plt.xlabel("Feature Importance Score")
# plt.ylabel("Feature")
# plt.title("Top 10 Features Influencing Sales Revenue Predictions")

# plt.tight_layout()


# plt.savefig(
#     OUTPUT_DIR / "feature_importance.png",
#     dpi=150,
#     bbox_inches="tight"
# )

# plt.close()

# print("Feature importance chart saved successfully.", flush=True)




# # ===================================
# # SECTION 6 - DATA VISUALISATION
# # ===================================

# print("\nSECTION 6 - DATA VISUALISATION")

# import matplotlib
# matplotlib.use("Agg")

# import matplotlib.pyplot as plt
# import seaborn as sns

# sns.set_theme(style="whitegrid")

# # CHART 1 - TOTAL SALES REVENUE BY REGION

# region_revenue = (
#     df.groupby("Region")["SalesRevenue"]
#     .sum()
#     .sort_values(ascending=False)
# )

# plt.figure(figsize=(9, 6))

# sns.barplot(
#     x=region_revenue.index,
#     y=region_revenue.values,
#     color="steelblue"
# )

# plt.title("Total Sales Revenue by Region")
# plt.xlabel("Region")
# plt.ylabel("Total Sales Revenue")
# plt.tight_layout()


# plt.savefig(OUTPUT_DIR / "revenue_by_region.png", dpi=150)
# plt.close()

# print("Chart 1 saved: revenue_by_region.png")


# # CHART 2 - AVERAGE SALES REVENUE BY SEASON

# season_order = ["Spring", "Summer", "Autumn", "Winter"]

# season_revenue = (
#     df.groupby("Season")["SalesRevenue"]
#     .mean()
#     .reindex(season_order)
# )

# plt.figure(figsize=(9, 6))

# sns.barplot(
#     x=season_revenue.index,
#     y=season_revenue.values,
#     color="seagreen"
# )

# plt.title("Average Sales Revenue by Season")
# plt.xlabel("Season")
# plt.ylabel("Average Sales Revenue")
# plt.tight_layout()


# plt.savefig(OUTPUT_DIR / "revenue_by_season.png", dpi=150)
# plt.close()

# print("Chart 2 saved: revenue_by_season.png")


# # CHART 3 - AVERAGE MARKETING EFFICIENCY BY REGION

# marketing_efficiency = (
#     df.groupby("Region")["MarketingEfficiency"]
#     .mean()
#     .sort_values(ascending=False)
# )

# plt.figure(figsize=(9, 6))

# sns.barplot(
#     x=marketing_efficiency.index,
#     y=marketing_efficiency.values,
#     color="mediumpurple"
# )

# plt.title("Average Marketing Efficiency by Region")
# plt.xlabel("Region")
# plt.ylabel("Sales Revenue / Marketing Spend")
# plt.tight_layout()

# plt.savefig(OUTPUT_DIR / "marketing_efficiency_by_region.png", dpi=150)
# plt.close()

# print("Chart 3 saved: marketing_efficiency_by_region.png")

# print("\nAll Section 6 charts saved successfully.")



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