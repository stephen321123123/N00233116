
# import pandas as pd

# # ==========================================
# # TASK 2 - RECOMMENDATION SYSTEM DEVELOPMENT
# # SECTION 1 - DATA PREPARATION & INTEGRATION
# # ==========================================

# print("\nSECTION 1 - DATA PREPARATION & INTEGRATION")

# # Load the three datasets
# customers = pd.read_csv("task2/data/Customers_repeat.csv")
# products = pd.read_csv("task2/data/Products_sort.csv")
# transactions = pd.read_csv("task2/data/Transactions_made.csv")

# # Inspect each dataset
# datasets = {
#     "CUSTOMERS": customers,
#     "PRODUCTS": products,
#     "TRANSACTIONS": transactions
# }

# for name, df in datasets.items():
#     print(f"\n========== {name} DATASET ==========")

#     print("\nFIRST FIVE ROWS:")
#     print(df.head().to_string())

#     print("\nDATASET SIZE:")
#     print(df.shape)

#     print("\nCOLUMN NAMES:")
#     print(df.columns.tolist())

#     print("\nDATA TYPES:")
#     print(df.dtypes.to_string())

#     print("\nMISSING VALUES:")
#     print(df.isnull().sum().to_string())

#     print("\nDUPLICATE ROWS:")
#     print(df.duplicated().sum())


# # ==========================================
# # SECTION 1 - DATA QUALITY INVESTIGATION
# # ==========================================

# print("\nDATA QUALITY INVESTIGATION")

# # Check inconsistent product categories
# print("\nPRODUCT CATEGORIES:")
# print(products["Category"].value_counts().to_string())

# # Check missing product ratings
# print("\nMISSING PRODUCT RATINGS:")
# print(products["Rating"].isnull().sum())

# print("\nMEDIAN PRODUCT RATING:")
# print(products["Rating"].median())

# # Investigate duplicate transactions
# print("\nEXACT DUPLICATE TRANSACTIONS:")
# print(transactions.duplicated().sum())

# print("\nSAMPLE DUPLICATE TRANSACTIONS:")
# print(
#     transactions[
#         transactions.duplicated(keep=False)
#     ].head(10).to_string(index=False)
# )

# # Check repeated customer-product combinations
# print("\nREPEATED CUSTOMER-PRODUCT PAIRS:")
# print(
#     transactions.duplicated(
#         subset=["CustomerID", "ProductID"]
#     ).sum()
# )

# # Check for transactions referencing missing customers/products
# print("\nUNKNOWN CUSTOMER IDS:")
# print(
#     (~transactions["CustomerID"].isin(
#         customers["CustomerID"]
#     )).sum()
# )

# print("\nUNKNOWN PRODUCT IDS:")
# print(
#     (~transactions["ProductID"].isin(
#         products["ProductID"]
#     )).sum()
# )



# # ==========================================
# # SECTION 1 - CLEANING & DATA INTEGRATION
# # ==========================================

# print("\nSECTION 1 - CLEANING & DATA INTEGRATION")

# # Create copies to preserve original data
# customers_clean = customers.copy()
# products_clean = products.copy()
# transactions_clean = transactions.copy()

# # Standardise product categories
# products_clean["Category"] = (
#     products_clean["Category"]
#     .str.strip()
#     .str.title()
# )

# # Fill missing ratings using the median
# median_rating = products_clean["Rating"].median()

# products_clean["Rating"] = (
#     products_clean["Rating"].fillna(median_rating)
# )

# # Preserve transaction records, including exact duplicates,
# # because there is no transaction ID to verify accidental copies.

# # Merge transactions with customers
# merged_data = transactions_clean.merge(
#     customers_clean,
#     on="CustomerID",
#     how="left",
#     validate="many_to_one"
# )

# # Merge with products
# merged_data = merged_data.merge(
#     products_clean,
#     on="ProductID",
#     how="left",
#     validate="many_to_one"
# )

# print("\nCLEANED PRODUCT CATEGORIES:")
# print(products_clean["Category"].value_counts())

# print("\nMISSING RATINGS AFTER CLEANING:")
# print(products_clean["Rating"].isnull().sum())

# print("\nMERGED DATASET SIZE:")
# print(merged_data.shape)

# print("\nMISSING VALUES AFTER MERGING:")
# print(merged_data.isnull().sum())

# # Create customer-product interaction matrix
# # PurchaseCount is used as the interaction strength.
# interaction_matrix = transactions_clean.pivot_table(
#     index="CustomerID",
#     columns="ProductID",
#     values="PurchaseCount",
#     aggfunc="sum",
#     fill_value=0
# )

# print("\nCUSTOMER-PRODUCT INTERACTION MATRIX SIZE:")
# print(interaction_matrix.shape)

# print("\nINTERACTION MATRIX SAMPLE:")
# print(interaction_matrix.iloc[:5, :10].to_string())

# # Save outputs
# products_clean.to_csv(
#     "task2/outputs/products_cleaned.csv",
#     index=False
# )

# merged_data.to_csv(
#     "task2/outputs/merged_recommendation_data.csv",
#     index=False
# )

# interaction_matrix.to_csv(
#     "task2/outputs/customer_product_matrix.csv"
# )

# print("\nSection 1 outputs saved successfully.")








# # ==========================================
# # SECTION 2 - CUSTOMER ANALYTICS
# # ==========================================

# print("\nSECTION 2 - CUSTOMER ANALYTICS")

# # Calculate purchasing statistics for each customer
# customer_summary = merged_data.groupby("CustomerID").agg(
#     TotalSpend=("Spend", "sum"),
#     TotalPurchases=("PurchaseCount", "sum"),
#     UniqueProducts=("ProductID", "nunique"),
#     TransactionRecords=("ProductID", "size")
# ).reset_index()

# # Add customer profile information
# customer_summary = customer_summary.merge(
#     customers_clean,
#     on="CustomerID",
#     how="left",
#     validate="one_to_one"
# )

# # TOP 10 CUSTOMERS BY SPENDING
# print("\nTOP 10 CUSTOMERS BY TOTAL SPEND")

# top_spenders = customer_summary.nlargest(
#     10, "TotalSpend"
# )

# print(
#     top_spenders[
#         ["CustomerID", "TotalSpend", "TotalPurchases",
#          "LoyaltyLevel", "Region"]
#     ].round(2).to_string(index=False)
# )

# # TOP 10 CUSTOMERS BY PURCHASE FREQUENCY
# print("\nTOP 10 CUSTOMERS BY PURCHASE COUNT")

# top_frequent = customer_summary.nlargest(
#     10, "TotalPurchases"
# )

# print(
#     top_frequent[
#         ["CustomerID", "TotalPurchases",
#          "UniqueProducts", "TotalSpend"]
#     ].round(2).to_string(index=False)
# )

# # IDENTIFY HIGH-VALUE CUSTOMERS
# high_value_threshold = customer_summary["TotalSpend"].quantile(0.75)

# customer_summary["CustomerValue"] = (
#     customer_summary["TotalSpend"].apply(
#         lambda x: "High Value"
#         if x >= high_value_threshold
#         else "Standard"
#     )
# )

# print("\nHIGH-VALUE CUSTOMER THRESHOLD:")
# print(round(high_value_threshold, 2))

# print("\nCUSTOMER VALUE DISTRIBUTION:")
# print(customer_summary["CustomerValue"].value_counts())

# # CUSTOMER SPENDING BY LOYALTY LEVEL
# print("\nCUSTOMER SPENDING BY LOYALTY LEVEL")

# loyalty_analysis = customer_summary.groupby(
#     "LoyaltyLevel"
# ).agg(
#     Customers=("CustomerID", "count"),
#     AverageSpend=("TotalSpend", "mean"),
#     TotalSpend=("TotalSpend", "sum")
# ).round(2)

# print(loyalty_analysis.to_string())

# # Save results
# customer_summary.to_csv(
#     "task2/outputs/customer_summary.csv",
#     index=False
# )

# top_spenders.to_csv(
#     "task2/outputs/top_10_customers_spend.csv",
#     index=False
# )

# top_frequent.to_csv(
#     "task2/outputs/top_10_customers_frequency.csv",
#     index=False
# )

# print("\nSection 2 customer analytics saved successfully.")




# # ==========================================
# # SECTION 3 - PRODUCT ANALYTICS
# # ==========================================

# print("\nSECTION 3 - PRODUCT ANALYTICS")

# # Calculate product performance
# product_summary = merged_data.groupby("ProductID").agg(
#     TotalRevenue=("Spend", "sum"),
#     TotalPurchases=("PurchaseCount", "sum"),
#     UniqueCustomers=("CustomerID", "nunique")
# ).reset_index()

# # Add product information
# product_summary = product_summary.merge(
#     products_clean,
#     on="ProductID",
#     how="left",
#     validate="one_to_one"
# )

# # TOP 10 PRODUCTS BY REVENUE
# print("\nTOP 10 PRODUCTS BY REVENUE")

# top_products = product_summary.nlargest(
#     10, "TotalRevenue"
# )

# print(
#     top_products[
#         ["ProductID", "Category", "Brand",
#          "TotalRevenue", "TotalPurchases"]
#     ].round(2).to_string(index=False)
# )

# # REVENUE BY PRODUCT CATEGORY
# print("\nREVENUE BY PRODUCT CATEGORY")

# category_analysis = product_summary.groupby(
#     "Category"
# ).agg(
#     TotalRevenue=("TotalRevenue", "sum"),
#     TotalPurchases=("TotalPurchases", "sum"),
#     ProductCount=("ProductID", "count")
# ).sort_values(
#     "TotalRevenue", ascending=False
# ).round(2)

# print(category_analysis.to_string())

# # REVENUE BY BRAND
# print("\nREVENUE BY BRAND")

# brand_analysis = product_summary.groupby(
#     "Brand"
# ).agg(
#     TotalRevenue=("TotalRevenue", "sum"),
#     TotalPurchases=("TotalPurchases", "sum"),
#     ProductCount=("ProductID", "count")
# ).sort_values(
#     "TotalRevenue", ascending=False
# ).round(2)

# print(brand_analysis.to_string())

# # SAVE RESULTS
# product_summary.to_csv(
#     "task2/outputs/product_summary.csv",
#     index=False
# )

# top_products.to_csv(
#     "task2/outputs/top_10_products.csv",
#     index=False
# )

# category_analysis.to_csv(
#     "task2/outputs/category_analysis.csv"
# )

# brand_analysis.to_csv(
#     "task2/outputs/brand_analysis.csv"
# )

# print("\nSection 3 product analytics saved successfully.")






# # ==========================================
# # SECTION 4 - GROUPBY & PIVOT TABLE ANALYSIS
# # ==========================================

# print("\nSECTION 4 - GROUPBY & PIVOT TABLE ANALYSIS")

# # GROUPBY 1 - Customer Spending by Region
# print("\nGROUPBY 1 - CUSTOMER SPENDING BY REGION")

# region_analysis = merged_data.groupby("Region").agg(
#     TotalRevenue=("Spend", "sum"),
#     TotalPurchases=("PurchaseCount", "sum"),
#     UniqueCustomers=("CustomerID", "nunique")
# ).sort_values("TotalRevenue", ascending=False).round(2)

# print(region_analysis.to_string())


# # GROUPBY 2 - Customer Spending by Age Group
# print("\nGROUPBY 2 - CUSTOMER SPENDING BY AGE GROUP")

# age_analysis = merged_data.groupby("AgeGroup").agg(
#     TotalRevenue=("Spend", "sum"),
#     TotalPurchases=("PurchaseCount", "sum"),
#     UniqueCustomers=("CustomerID", "nunique")
# ).sort_values("TotalRevenue", ascending=False).round(2)

# print(age_analysis.to_string())


# # GROUPBY 3 - Product Category by Loyalty Level
# print("\nGROUPBY 3 - PRODUCT CATEGORY BY LOYALTY LEVEL")

# loyalty_category_analysis = merged_data.groupby(
#     ["LoyaltyLevel", "Category"]
# ).agg(
#     TotalRevenue=("Spend", "sum"),
#     TotalPurchases=("PurchaseCount", "sum")
# ).round(2)

# print(loyalty_category_analysis.to_string())


# # PIVOT TABLE 1 - Revenue by Region and Category
# print("\nPIVOT TABLE 1 - REVENUE BY REGION AND CATEGORY")

# pivot1 = pd.pivot_table(
#     merged_data,
#     values="Spend",
#     index="Region",
#     columns="Category",
#     aggfunc="sum",
#     fill_value=0
# ).round(2)

# print(pivot1.to_string())


# # PIVOT TABLE 2 - Revenue by Loyalty Level and Age Group
# print("\nPIVOT TABLE 2 - REVENUE BY LOYALTY LEVEL AND AGE GROUP")

# pivot2 = pd.pivot_table(
#     merged_data,
#     values="Spend",
#     index="LoyaltyLevel",
#     columns="AgeGroup",
#     aggfunc="sum",
#     fill_value=0
# ).round(2)

# print(pivot2.to_string())


# # SAVE SECTION 4 RESULTS

# region_analysis.to_csv(
#     "task2/outputs/revenue_by_region.csv"
# )

# age_analysis.to_csv(
#     "task2/outputs/revenue_by_age_group.csv"
# )

# loyalty_category_analysis.to_csv(
#     "task2/outputs/loyalty_category_analysis.csv"
# )

# pivot1.to_csv(
#     "task2/outputs/pivot_region_category.csv"
# )

# pivot2.to_csv(
#     "task2/outputs/pivot_loyalty_age.csv"
# )

# print("\nSection 4 outputs saved successfully.")





# # ==========================================
# # SECTION 5 - RECOMMENDATION SYSTEM DEVELOPMENT
# # ==========================================

# print("\nSECTION 5 - RECOMMENDATION SYSTEM DEVELOPMENT")

# from sklearn.metrics.pairwise import cosine_similarity

# # ------------------------------------------
# # RECOMMENDATION SYSTEM 1 - POPULARITY BASED
# # ------------------------------------------

# print("\nRECOMMENDATION SYSTEM 1 - POPULARITY BASED")

# # Calculate overall product popularity using purchase counts
# product_popularity = interaction_matrix.sum(axis=0).sort_values(
#     ascending=False
# )

# print("\nTOP 10 MOST POPULAR PRODUCTS:")
# print(product_popularity.head(10).to_string())


# def popularity_recommendations(customer_id, n=5):
#     # Products already purchased by this customer
#     purchased_products = set(
#         interaction_matrix.columns[
#             interaction_matrix.loc[customer_id] > 0
#         ]
#     )

#     # Exclude previously purchased products
#     recommendations = product_popularity[
#         ~product_popularity.index.isin(purchased_products)
#     ]

#     return recommendations.head(n).index.tolist()


# # ------------------------------------------
# # RECOMMENDATION SYSTEM 2 - COLLABORATIVE FILTERING
# # ------------------------------------------

# print("\nRECOMMENDATION SYSTEM 2 - COLLABORATIVE FILTERING")

# # Calculate similarity between customers
# similarity_matrix = cosine_similarity(interaction_matrix)

# # Convert to a DataFrame with customer IDs
# customer_similarity = pd.DataFrame(
#     similarity_matrix,
#     index=interaction_matrix.index,
#     columns=interaction_matrix.index
# )

# print("\nCUSTOMER SIMILARITY MATRIX SIZE:")
# print(customer_similarity.shape)


# def collaborative_recommendations(customer_id, n=5):

#     # Find similarities for the selected customer
#     similarities = customer_similarity.loc[customer_id].copy()

#     # Exclude the customer themselves
#     similarities = similarities.drop(customer_id)

#     # Select the 10 most similar customers
#     similar_customers = similarities.nlargest(10)

#     # Get purchasing behaviour of similar customers
#     similar_purchases = interaction_matrix.loc[
#         similar_customers.index
#     ]

#     # Calculate weighted recommendation scores
#     weighted_scores = similar_purchases.mul(
#         similar_customers, axis=0
#     ).sum(axis=0)

#     # Exclude products already purchased
#     purchased_products = interaction_matrix.loc[customer_id] > 0

#     weighted_scores = weighted_scores[
#         ~purchased_products
#     ]

#     # Recommend products with positive scores
#     weighted_scores = weighted_scores[
#         weighted_scores > 0
#     ].sort_values(ascending=False)

#     return weighted_scores.head(n).index.tolist()


# # ------------------------------------------
# # GENERATE RECOMMENDATIONS FOR 5 CUSTOMERS
# # ------------------------------------------

# example_customers = [1, 25, 100, 250, 500]

# print("\nRECOMMENDATIONS FOR FIVE EXAMPLE CUSTOMERS")

# recommendation_results = []

# for customer_id in example_customers:

#     popular = popularity_recommendations(customer_id)
#     collaborative = collaborative_recommendations(customer_id)

#     print(f"\nCUSTOMER {customer_id}")
#     print("Popularity-Based:", popular)
#     print("Collaborative Filtering:", collaborative)

#     recommendation_results.append({
#         "CustomerID": customer_id,
#         "PopularityRecommendations": str(popular),
#         "CollaborativeRecommendations": str(collaborative)
#     })


# # ------------------------------------------
# # SAVE SECTION 5 RESULTS
# # ------------------------------------------

# recommendation_df = pd.DataFrame(recommendation_results)

# recommendation_df.to_csv(
#     "task2/outputs/recommendation_results.csv",
#     index=False
# )

# product_popularity.to_csv(
#     "task2/outputs/product_popularity.csv",
#     header=["TotalPurchases"]
# )

# customer_similarity.to_csv(
#     "task2/outputs/customer_similarity.csv"
# )

# print("\nSection 5 recommendation systems saved successfully.")






# # ==========================================
# # SECTION 6 - RECOMMENDATION EVALUATION
# # ==========================================

# print("\nSECTION 6 - RECOMMENDATION EVALUATION")

# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# # Create a training copy of the interaction matrix
# train_matrix = interaction_matrix.copy()

# # Randomly hide one purchased product per eligible customer
# rng = np.random.default_rng(42)
# test_products = {}

# for customer_id in train_matrix.index:

#     purchased = train_matrix.columns[
#         train_matrix.loc[customer_id] > 0
#     ].to_numpy()

#     if len(purchased) >= 2:
#         hidden_product = int(rng.choice(purchased))

#         test_products[customer_id] = hidden_product
#         train_matrix.loc[customer_id, hidden_product] = 0

# print("\nCUSTOMERS ELIGIBLE FOR EVALUATION:")
# print(len(test_products))


# # ------------------------------------------
# # REBUILD ALGORITHMS USING TRAINING DATA
# # ------------------------------------------

# train_popularity = train_matrix.sum(axis=0).sort_values(
#     ascending=False
# )

# train_similarity = pd.DataFrame(
#     cosine_similarity(train_matrix),
#     index=train_matrix.index,
#     columns=train_matrix.index
# )


# def evaluate_popularity(customer_id, n=5):

#     purchased = train_matrix.loc[customer_id] > 0

#     scores = train_popularity[~purchased]

#     return scores.head(n).index.tolist()


# def evaluate_collaborative(customer_id, n=5):

#     similarities = train_similarity.loc[customer_id].drop(
#         customer_id
#     )

#     neighbours = similarities.nlargest(10)

#     neighbour_purchases = train_matrix.loc[
#         neighbours.index
#     ]

#     scores = neighbour_purchases.mul(
#         neighbours, axis=0
#     ).sum(axis=0)

#     purchased = train_matrix.loc[customer_id] > 0

#     scores = scores[~purchased]

#     scores = scores[
#         scores > 0
#     ].sort_values(ascending=False)

#     return scores.head(n).index.tolist()


# # ------------------------------------------
# # EVALUATE BOTH ALGORITHMS
# # ------------------------------------------

# popularity_hits = 0
# collaborative_hits = 0

# popularity_products = set()
# collaborative_products = set()

# overlap_scores = []
# evaluation_rows = []

# for customer_id, hidden_product in test_products.items():

#     popular = evaluate_popularity(customer_id)
#     collaborative = evaluate_collaborative(customer_id)

#     pop_hit = int(hidden_product in popular)
#     collab_hit = int(hidden_product in collaborative)

#     popularity_hits += pop_hit
#     collaborative_hits += collab_hit

#     popularity_products.update(popular)
#     collaborative_products.update(collaborative)

#     overlap = len(set(popular) & set(collaborative))
#     overlap_scores.append(overlap)

#     evaluation_rows.append({
#         "CustomerID": customer_id,
#         "HiddenProduct": hidden_product,
#         "PopularityHit": pop_hit,
#         "CollaborativeHit": collab_hit,
#         "PopularityRecommendations": str(popular),
#         "CollaborativeRecommendations": str(collaborative)
#     })


# # ------------------------------------------
# # CALCULATE EVALUATION METRICS
# # ------------------------------------------

# total_customers = len(test_products)
# total_products = train_matrix.shape[1]

# popularity_hit_rate = popularity_hits / total_customers
# collaborative_hit_rate = collaborative_hits / total_customers

# popularity_coverage = (
#     len(popularity_products) / total_products
# )

# collaborative_coverage = (
#     len(collaborative_products) / total_products
# )

# average_overlap = np.mean(overlap_scores)


# # ------------------------------------------
# # PRINT EVALUATION RESULTS
# # ------------------------------------------

# print("\nRECOMMENDATION EVALUATION RESULTS")

# print(f"\nPopularity Hit Rate@5: {popularity_hit_rate:.4f}")
# print(f"Collaborative Hit Rate@5: {collaborative_hit_rate:.4f}")

# print(f"\nPopularity Coverage@5: {popularity_coverage:.4f}")
# print(f"Collaborative Coverage@5: {collaborative_coverage:.4f}")

# print(f"\nAverage Recommendation Overlap@5: {average_overlap:.2f}")

# print("\nTOTAL SUCCESSFUL PREDICTIONS")
# print("Popularity-Based:", popularity_hits)
# print("Collaborative Filtering:", collaborative_hits)


# # ------------------------------------------
# # ALGORITHM COMPARISON
# # ------------------------------------------

# comparison = pd.DataFrame({
#     "Algorithm": [
#         "Popularity-Based",
#         "Collaborative Filtering"
#     ],
#     "HitRateAt5": [
#         popularity_hit_rate,
#         collaborative_hit_rate
#     ],
#     "CoverageAt5": [
#         popularity_coverage,
#         collaborative_coverage
#     ]
# })

# print("\nALGORITHM COMPARISON")
# print(comparison.round(4).to_string(index=False))


# # ------------------------------------------
# # SAVE RESULTS
# # ------------------------------------------

# comparison.to_csv(
#     "task2/outputs/recommendation_comparison.csv",
#     index=False
# )

# pd.DataFrame(evaluation_rows).to_csv(
#     "task2/outputs/recommendation_evaluation.csv",
#     index=False
# )

# print("\nSection 6 evaluation saved successfully.")
