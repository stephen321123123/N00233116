from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parent
DATA, OUT = BASE / 'data', BASE / 'outputs'
OUT.mkdir(exist_ok=True)


def show(title, value):
    print(f'\n{title}')
    print(value.to_string() if isinstance(value, (pd.DataFrame, pd.Series)) else value)


def save(filename, table, index=True):
    table.to_csv(OUT / filename, index=index)


def recommend_popular(customer, matrix, ranking, n=5):
    return ranking[matrix.loc[customer, ranking.index].eq(0)].head(n).index.tolist()


def recommend_collaborative(customer, matrix, similarities, n=5):
    neighbours = similarities.loc[customer].drop(customer).nlargest(10)
    scores = matrix.loc[neighbours.index].mul(neighbours, axis=0).sum(axis=0)
    scores = scores[(matrix.loc[customer] == 0) & (scores > 0)]
    return scores.sort_values(ascending=False).head(n).index.tolist()


# SECTION 1 - DATA PREPARATION AND INTEGRATION
print('\nSECTION 1 - DATA PREPARATION & INTEGRATION')
customers = pd.read_csv(DATA / 'Customers_repeat.csv')
products = pd.read_csv(DATA / 'Products_sort.csv')
transactions = pd.read_csv(DATA / 'Transactions_made.csv')
for name, data in [('CUSTOMERS', customers), ('PRODUCTS', products), ('TRANSACTIONS', transactions)]:
    print(f'\n========== {name} DATASET ==========')
    show('FIRST FIVE ROWS:', data.head())
    show('DATASET SIZE:', data.shape)
    show('COLUMN NAMES:', data.columns.tolist())
    show('DATA TYPES:', data.dtypes)
    show('MISSING VALUES:', data.isna().sum())
    show('DUPLICATE ROWS:', data.duplicated().sum())

show('PRODUCT CATEGORIES:', products['Category'].value_counts())
show('MISSING PRODUCT RATINGS:', products['Rating'].isna().sum())
show('MEDIAN PRODUCT RATING:', products['Rating'].median())
show('EXACT DUPLICATE TRANSACTIONS:', transactions.duplicated().sum())
show('SAMPLE DUPLICATE TRANSACTIONS:', transactions[transactions.duplicated(keep=False)].head(10))
show('REPEATED CUSTOMER-PRODUCT PAIRS:', transactions.duplicated(['CustomerID', 'ProductID']).sum())
show('UNKNOWN CUSTOMER IDS:', (~transactions.CustomerID.isin(customers.CustomerID)).sum())
show('UNKNOWN PRODUCT IDS:', (~transactions.ProductID.isin(products.ProductID)).sum())

# Keep duplicate transaction rows: no transaction ID exists to verify accidental copies.
products_clean = products.copy()
products_clean['Category'] = products_clean['Category'].str.strip().str.title()
products_clean['Rating'] = products_clean['Rating'].fillna(products_clean['Rating'].median())
merged_data = (transactions.merge(customers, on='CustomerID', how='left', validate='many_to_one')
               .merge(products_clean, on='ProductID', how='left', validate='many_to_one'))
interaction_matrix = transactions.pivot_table(index='CustomerID', columns='ProductID',
                                              values='PurchaseCount', aggfunc='sum', fill_value=0)
show('CLEANED PRODUCT CATEGORIES:', products_clean.Category.value_counts())
show('MISSING RATINGS AFTER CLEANING:', products_clean.Rating.isna().sum())
show('MERGED DATASET SIZE:', merged_data.shape)
show('MISSING VALUES AFTER MERGING:', merged_data.isna().sum())
show('CUSTOMER-PRODUCT INTERACTION MATRIX SIZE:', interaction_matrix.shape)
show('INTERACTION MATRIX SAMPLE:', interaction_matrix.iloc[:5, :10])
save('products_cleaned.csv', products_clean, False)
save('merged_recommendation_data.csv', merged_data, False)
save('customer_product_matrix.csv', interaction_matrix)
print('\nSection 1 outputs saved successfully.')


# SECTION 2 - CUSTOMER ANALYTICS
print('\nSECTION 2 - CUSTOMER ANALYTICS')
customer_summary = (merged_data.groupby('CustomerID').agg(
    TotalSpend=('Spend', 'sum'), TotalPurchases=('PurchaseCount', 'sum'),
    UniqueProducts=('ProductID', 'nunique'), TransactionRecords=('ProductID', 'size'))
    .reset_index().merge(customers, on='CustomerID', how='left', validate='one_to_one'))
top_spenders = customer_summary.nlargest(10, 'TotalSpend')
top_frequent = customer_summary.nlargest(10, 'TotalPurchases')
show('TOP 10 CUSTOMERS BY TOTAL SPEND:', top_spenders[
    ['CustomerID', 'TotalSpend', 'TotalPurchases', 'LoyaltyLevel', 'Region']].round(2))
show('TOP 10 CUSTOMERS BY PURCHASE COUNT:', top_frequent[
    ['CustomerID', 'TotalPurchases', 'UniqueProducts', 'TotalSpend']].round(2))
threshold = customer_summary.TotalSpend.quantile(.75)
customer_summary['CustomerValue'] = np.where(customer_summary.TotalSpend >= threshold, 'High Value', 'Standard')
show('HIGH-VALUE CUSTOMER THRESHOLD:', round(threshold, 2))
show('CUSTOMER VALUE DISTRIBUTION:', customer_summary.CustomerValue.value_counts())
loyalty_analysis = customer_summary.groupby('LoyaltyLevel').agg(
    Customers=('CustomerID', 'count'), AverageSpend=('TotalSpend', 'mean'),
    TotalSpend=('TotalSpend', 'sum')).round(2)
show('CUSTOMER SPENDING BY LOYALTY LEVEL:', loyalty_analysis)
for name, data in [('customer_summary.csv', customer_summary),
                   ('top_10_customers_spend.csv', top_spenders),
                   ('top_10_customers_frequency.csv', top_frequent)]:
    save(name, data, False)
print('\nSection 2 customer analytics saved successfully.')


# SECTION 3 - PRODUCT ANALYTICS
print('\nSECTION 3 - PRODUCT ANALYTICS')
product_summary = (merged_data.groupby('ProductID').agg(
    TotalRevenue=('Spend', 'sum'), TotalPurchases=('PurchaseCount', 'sum'),
    UniqueCustomers=('CustomerID', 'nunique')).reset_index()
    .merge(products_clean, on='ProductID', how='left', validate='one_to_one'))
top_products = product_summary.nlargest(10, 'TotalRevenue')
show('TOP 10 PRODUCTS BY REVENUE:', top_products[
    ['ProductID', 'Category', 'Brand', 'TotalRevenue', 'TotalPurchases']].round(2))
product_aggregation = dict(TotalRevenue=('TotalRevenue', 'sum'),
                           TotalPurchases=('TotalPurchases', 'sum'), ProductCount=('ProductID', 'count'))
category_analysis = product_summary.groupby('Category').agg(**product_aggregation).sort_values('TotalRevenue', ascending=False).round(2)
brand_analysis = product_summary.groupby('Brand').agg(**product_aggregation).sort_values('TotalRevenue', ascending=False).round(2)
show('REVENUE BY PRODUCT CATEGORY:', category_analysis)
show('REVENUE BY BRAND:', brand_analysis)
for name, data, index in [('product_summary.csv', product_summary, False),
                          ('top_10_products.csv', top_products, False),
                          ('category_analysis.csv', category_analysis, True),
                          ('brand_analysis.csv', brand_analysis, True)]:
    save(name, data, index)
print('\nSection 3 product analytics saved successfully.')


# SECTION 4 - GROUPBY AND PIVOT TABLE ANALYSIS
print('\nSECTION 4 - GROUPBY & PIVOT TABLE ANALYSIS')
regional_age_aggregation = dict(TotalRevenue=('Spend', 'sum'),
                                TotalPurchases=('PurchaseCount', 'sum'), UniqueCustomers=('CustomerID', 'nunique'))
region_analysis = merged_data.groupby('Region').agg(**regional_age_aggregation).sort_values('TotalRevenue', ascending=False).round(2)
age_analysis = merged_data.groupby('AgeGroup').agg(**regional_age_aggregation).sort_values('TotalRevenue', ascending=False).round(2)
loyalty_category_analysis = merged_data.groupby(['LoyaltyLevel', 'Category']).agg(
    TotalRevenue=('Spend', 'sum'), TotalPurchases=('PurchaseCount', 'sum')).round(2)
pivot1 = pd.pivot_table(merged_data, values='Spend', index='Region', columns='Category', aggfunc='sum', fill_value=0).round(2)
pivot2 = pd.pivot_table(merged_data, values='Spend', index='LoyaltyLevel', columns='AgeGroup', aggfunc='sum', fill_value=0).round(2)
for title, filename, table in [
    ('GROUPBY 1 - CUSTOMER SPENDING BY REGION:', 'revenue_by_region.csv', region_analysis),
    ('GROUPBY 2 - CUSTOMER SPENDING BY AGE GROUP:', 'revenue_by_age_group.csv', age_analysis),
    ('GROUPBY 3 - PRODUCT CATEGORY BY LOYALTY LEVEL:', 'loyalty_category_analysis.csv', loyalty_category_analysis),
    ('PIVOT TABLE 1 - REVENUE BY REGION AND CATEGORY:', 'pivot_region_category.csv', pivot1),
    ('PIVOT TABLE 2 - REVENUE BY LOYALTY LEVEL AND AGE GROUP:', 'pivot_loyalty_age.csv', pivot2)]:
    show(title, table)
    save(filename, table)
print('\nSection 4 outputs saved successfully.')


# SECTION 5 - RECOMMENDATION SYSTEM DEVELOPMENT
print('\nSECTION 5 - RECOMMENDATION SYSTEM DEVELOPMENT')
product_popularity = interaction_matrix.sum(axis=0).sort_values(ascending=False)
customer_similarity = pd.DataFrame(cosine_similarity(interaction_matrix),
                                   index=interaction_matrix.index, columns=interaction_matrix.index)
show('TOP 10 MOST POPULAR PRODUCTS:', product_popularity.head(10))
show('CUSTOMER SIMILARITY MATRIX SIZE:', customer_similarity.shape)
recommendation_results = []
print('\nRECOMMENDATIONS FOR FIVE EXAMPLE CUSTOMERS')
for customer in [1, 25, 100, 250, 500]:
    popular = recommend_popular(customer, interaction_matrix, product_popularity)
    collaborative = recommend_collaborative(customer, interaction_matrix, customer_similarity)
    print(f'\nCUSTOMER {customer}\nPopularity-Based: {popular}\nCollaborative Filtering: {collaborative}')
    recommendation_results.append(dict(CustomerID=customer, PopularityRecommendations=str(popular),
                                       CollaborativeRecommendations=str(collaborative)))
save('recommendation_results.csv', pd.DataFrame(recommendation_results), False)
save('product_popularity.csv', product_popularity.rename('TotalPurchases'))
save('customer_similarity.csv', customer_similarity)
print('\nSection 5 recommendation systems saved successfully.')


# SECTION 6 - RECOMMENDATION EVALUATION
print('\nSECTION 6 - RECOMMENDATION EVALUATION')
train_matrix = interaction_matrix.copy()
rng = np.random.default_rng(42)
test_products = {}
for customer in train_matrix.index:
    purchased = train_matrix.columns[train_matrix.loc[customer] > 0].to_numpy()
    if len(purchased) >= 2:
        hidden = int(rng.choice(purchased))
        test_products[customer] = hidden
        train_matrix.loc[customer, hidden] = 0
show('CUSTOMERS ELIGIBLE FOR EVALUATION:', len(test_products))
train_popularity = train_matrix.sum(axis=0).sort_values(ascending=False)
train_similarity = pd.DataFrame(cosine_similarity(train_matrix),
                                index=train_matrix.index, columns=train_matrix.index)
evaluation_rows = []
recommended_products = {'Popularity-Based': set(), 'Collaborative Filtering': set()}
overlap_scores = []
for customer, hidden in test_products.items():
    popular = recommend_popular(customer, train_matrix, train_popularity)
    collaborative = recommend_collaborative(customer, train_matrix, train_similarity)
    recommended_products['Popularity-Based'].update(popular)
    recommended_products['Collaborative Filtering'].update(collaborative)
    overlap_scores.append(len(set(popular) & set(collaborative)))
    evaluation_rows.append(dict(CustomerID=customer, HiddenProduct=hidden,
                                PopularityHit=int(hidden in popular), CollaborativeHit=int(hidden in collaborative),
                                PopularityRecommendations=str(popular), CollaborativeRecommendations=str(collaborative)))
evaluation_df = pd.DataFrame(evaluation_rows)
total = len(test_products)
comparison = pd.DataFrame([
    dict(Algorithm='Popularity-Based', HitRateAt5=evaluation_df.PopularityHit.sum() / total,
         CoverageAt5=len(recommended_products['Popularity-Based']) / train_matrix.shape[1]),
    dict(Algorithm='Collaborative Filtering', HitRateAt5=evaluation_df.CollaborativeHit.sum() / total,
         CoverageAt5=len(recommended_products['Collaborative Filtering']) / train_matrix.shape[1])
])
print('\nRECOMMENDATION EVALUATION RESULTS')
for row in comparison.itertuples():
    print(f'{row.Algorithm} Hit Rate@5: {row.HitRateAt5:.4f}')
    print(f'{row.Algorithm} Coverage@5: {row.CoverageAt5:.4f}')
show('Average Recommendation Overlap@5:', f'{np.mean(overlap_scores):.2f}')
show('TOTAL SUCCESSFUL PREDICTIONS:',
     f'Popularity-Based: {evaluation_df.PopularityHit.sum()}\nCollaborative Filtering: {evaluation_df.CollaborativeHit.sum()}')
show('ALGORITHM COMPARISON:', comparison.round(4))
save('recommendation_comparison.csv', comparison, False)
save('recommendation_evaluation.csv', evaluation_df, False)
print('\nSection 6 evaluation saved successfully.')



# ============================================================
# SECTION 7 – VISUALISATIONS
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

output_dir = Path(__file__).resolve().parent / "outputs"

# GRAPH 1 – CUSTOMER SPENDING DISTRIBUTION
customers = pd.read_csv(output_dir / "customer_summary.csv")

plt.figure(figsize=(9, 5))
plt.hist(customers["TotalSpend"], bins=25, edgecolor="black")
plt.title("Customer Spending Distribution")
plt.xlabel("Total Customer Spend")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(output_dir / "customer_spending_distribution.png", dpi=300)
plt.close()

# GRAPH 2 – RECOMMENDATION ALGORITHM COMPARISON
comparison = pd.read_csv(output_dir / "recommendation_comparison.csv")

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].bar(comparison["Algorithm"], comparison["HitRateAt5"] * 100)
axes[0].set_title("Hit Rate@5 Comparison")
axes[0].set_ylabel("Hit Rate (%)")
axes[0].set_ylim(0, 100)

axes[1].bar(comparison["Algorithm"], comparison["CoverageAt5"] * 100)
axes[1].set_title("Coverage@5 Comparison")
axes[1].set_ylabel("Coverage (%)")
axes[1].set_ylim(0, 100)

for ax in axes:
    ax.tick_params(axis="x", labelrotation=15)
    for bar in ax.patches:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{bar.get_height():.1f}%",
            ha="center"
        )

plt.tight_layout()
plt.savefig(output_dir / "recommendation_comparison.png", dpi=300)
plt.close()

# GRAPH 3 – REVENUE BY PRODUCT CATEGORY
categories = pd.read_csv(output_dir / "category_analysis.csv")
categories = categories.sort_values("TotalRevenue")

plt.figure(figsize=(9, 5))
plt.barh(categories["Category"], categories["TotalRevenue"])
plt.title("Revenue by Product Category")
plt.xlabel("Total Revenue")
plt.ylabel("Product Category")
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"{x / 1_000_000:.1f}M")
)
plt.tight_layout()
plt.savefig(output_dir / "revenue_by_product_category.png", dpi=300)
plt.close()

print("\nSECTION 7 – VISUALISATIONS COMPLETE")
print("Saved 3 graphs to:", output_dir)
