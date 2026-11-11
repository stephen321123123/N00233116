
import pandas as pd

# Load the retail dataset
df = pd.read_csv("Retail_outlets.csv")

# Display the first five rows
print("\nFIRST FIVE ROWS:")
print(df.head().to_string())

# Display dataset dimensions
print("\nDATASET SIZE:")
print(df.shape)

# Display column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# Check data types
print("\nDATA TYPES:")
print(df.dtypes)

# Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())

# Display summary statistics
print("\nSUMMARY STATISTICS:")
print(df.describe().to_string())



# Remove duplicate rows
df = df.drop_duplicates().copy()

# Check the results
print("\nAFTER REMOVING DUPLICATES:")
print("Remaining rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())


# -----------------------------------
# MISSING VALUE ANALYSIS
# -----------------------------------

# Check missing values after removing duplicates
print("\nMISSING VALUES AFTER DUPLICATE REMOVAL:")
print(df.isnull().sum())

# Calculate percentage of missing values
print("\nMISSING VALUE PERCENTAGES:")
print((df.isnull().mean() * 100).round(2))


# -----------------------------------
# HANDLE MISSING VALUES
# -----------------------------------

# Columns containing missing numerical values
missing_columns = [
    "MarketingSpend",
    "OnlineTraffic",
    "CustomerSatisfaction",
    "InventoryAvailability"
]

# Replace missing values with each column's median
for column in missing_columns:
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)

    print(f"{column}: filled missing values with median {median_value:.2f}")

# Verify that missing values have been handled
print("\nMISSING VALUES AFTER CLEANING:")
print(df.isnull().sum())

print("\nDATASET SIZE AFTER CLEANING:")
print(df.shape)


# -----------------------------------
# OUTLIER INVESTIGATION
# -----------------------------------

# Select numerical columns to investigate
outlier_columns = [
    "MarketingSpend",
    "Footfall",
    "OnlineTraffic",
    "StaffHours",
    "SalesRevenue"
]

print("\nOUTLIER INVESTIGATION (IQR METHOD):")

for column in outlier_columns:

    # Calculate the first and third quartiles
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the interquartile range
    IQR = Q3 - Q1

    # Calculate lower and upper boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find values outside the boundaries
    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(f"\n{column}")
    print(f"Lower bound: {lower_bound:.2f}")
    print(f"Upper bound: {upper_bound:.2f}")
    print(f"Number of outliers: {len(outliers)}")

    
# -----------------------------------
# FEATURE ENGINEERING
# -----------------------------------

# Feature 1: Revenue generated per visitor
df["RevenuePerVisitor"] = (
    df["SalesRevenue"] / df["Footfall"].replace(0, float("nan"))
)

# Feature 2: Revenue relative to marketing spend
df["MarketingEfficiency"] = (
    df["SalesRevenue"] / df["MarketingSpend"].replace(0, float("nan"))
)

# Feature 3: Percentage change from previous month's sales
df["SalesGrowthPercent"] = (
    (df["SalesRevenue"] - df["PreviousMonthSales"])
    / df["PreviousMonthSales"].replace(0, float("nan"))
) * 100

# Display the new features
print("\nFEATURE ENGINEERING RESULTS:")

print(df[
    [
        "RevenuePerVisitor",
        "MarketingEfficiency",
        "SalesGrowthPercent"
    ]
].head(10).round(2).to_string())

# Verify dataset dimensions
print("\nDATASET SIZE AFTER FEATURE ENGINEERING:")
print(df.shape)

# Check for missing values in engineered features
print("\nMISSING VALUES IN NEW FEATURES:")
print(df[
    [
        "RevenuePerVisitor",
        "MarketingEfficiency",
        "SalesGrowthPercent"
    ]
].isnull().sum())


# Save cleaned dataset with engineered features
df.to_csv("Retail_outlets_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully.")

