import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# =====================================
# 1. LOAD DATASET
# =====================================

df = pd.read_excel("Online Retail.xlsx")

print("ORIGINAL DATASET SHAPE:", df.shape)

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS:")
print(df.duplicated().sum())

# =====================================
# DUPLICATE RECORD INVESTIGATION
# =====================================

duplicate_rows = df[df.duplicated(keep=False)]

print("\nDUPLICATE INVESTIGATION:")
print("Total duplicate rows (including original occurrences):", len(duplicate_rows))
print("Exact duplicate records beyond first occurrences:", df.duplicated().sum())

print("\nSAMPLE DUPLICATE RECORDS:")
print(duplicate_rows.head(10).to_string(index=False))

# =====================================
# DUPLICATE IMPACT ANALYSIS
# =====================================

df_without_duplicates = df.drop_duplicates()

print("\nDUPLICATE IMPACT ANALYSIS:")
print("Original rows:", len(df))
print("Rows after removing duplicates:", len(df_without_duplicates))
print("Duplicate rows removed:", len(df) - len(df_without_duplicates))

print("Original positive transaction revenue:",
      (df.loc[(df["Quantity"] > 0) & (df["UnitPrice"] > 0), "Quantity"] *
       df.loc[(df["Quantity"] > 0) & (df["UnitPrice"] > 0), "UnitPrice"]).sum())

print("Revenue after duplicate removal:",
      (df_without_duplicates.loc[(df_without_duplicates["Quantity"] > 0) & (df_without_duplicates["UnitPrice"] > 0), "Quantity"] *
       df_without_duplicates.loc[(df_without_duplicates["Quantity"] > 0) & (df_without_duplicates["UnitPrice"] > 0), "UnitPrice"]).sum())

# =====================================
# 2. DATA CLEANING
# =====================================

# Remove exact duplicate records
df_clean = df.drop_duplicates().copy()

# Remove rows with missing CustomerID or Description
df_clean = df_clean.dropna(
    subset=["CustomerID", "Description"]
).copy()

# Remove cancelled transactions
df_clean = df_clean[
    ~df_clean["InvoiceNo"].astype(str).str.startswith("C")
].copy()

# Remove invalid quantities and prices
df_clean = df_clean[
    (df_clean["Quantity"] > 0) &
    (df_clean["UnitPrice"] > 0)
].copy()

# Calculate revenue
df_clean["Revenue"] = (
    df_clean["Quantity"] * df_clean["UnitPrice"]
)

print("\nCLEANED DATASET SHAPE:", df_clean.shape)

print("\nFIRST FIVE CLEANED RECORDS:")
print(df_clean.head())

print("\nTOTAL REVENUE FROM CLEANED RECORDS:")
print("£", round(df_clean["Revenue"].sum(), 2))

print("\nUNIQUE CUSTOMERS:")
print(df_clean["CustomerID"].nunique())

print("\nUNIQUE PRODUCTS:")
print(df_clean["StockCode"].nunique())

print("\nCOUNTRIES:")
print(df_clean["Country"].nunique())


# =====================================
# 3. BUSINESS PERFORMANCE ANALYSIS
# =====================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Month"] = df["InvoiceDate"].dt.to_period("M")

df_clean["Month"] = df_clean["InvoiceDate"].dt.to_period("M")
# Monthly revenue
monthly_revenue = (
    df_clean.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\nMONTHLY REVENUE:")
print(monthly_revenue)


# Top 10 products
top_products = (
    df_clean.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTS BY REVENUE:")
print(top_products)


# Top 10 countries
top_countries = (
    df_clean.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 COUNTRIES BY REVENUE:")
print(top_countries)


# Top 10 customers
top_customers = (
    df_clean.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 CUSTOMERS BY REVENUE:")
print(top_customers)


# Repeat customer analysis
customer_orders = (
    df_clean.groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

repeat_customers = (customer_orders > 1).sum()

repeat_rate = (
    repeat_customers / len(customer_orders)
) * 100

print("\nREPEAT CUSTOMER ANALYSIS:")
print("Total customers:", len(customer_orders))
print("Repeat customers:", repeat_customers)
print("Repeat customer rate:", round(repeat_rate, 2), "%")


# =====================================
# 4. VISUALISATION SETTINGS
# =====================================

sns.set_theme(style="whitegrid")


# =====================================
# 5. MONTHLY REVENUE PERFORMANCE
# =====================================

fig, ax = plt.subplots(figsize=(13, 7))

monthly_revenue.plot(
    kind="line",
    marker="o",
    linewidth=2.5,
    markersize=7,
    ax=ax
)

# Identify highest revenue month
highest_month = monthly_revenue.idxmax()
highest_revenue = monthly_revenue.max()

# Highlight peak without covering the line
ax.annotate(
    f"Peak: £{highest_revenue:,.0f}",
    xy=(highest_month, highest_revenue),
    xytext=(-65, 45),
    textcoords="offset points",
    fontsize=11,
    fontweight="bold",
    ha="center",
    arrowprops=dict(
        arrowstyle="->",
        connectionstyle="arc3,rad=0.2"
    ),
    bbox=dict(
        boxstyle="round,pad=0.5",
        fc="white",
        ec="gray",
        alpha=0.95
    )
)

fig.suptitle(
    "Monthly Revenue Performance",
    fontsize=20,
    fontweight="bold",
    y=0.97
)

fig.text(
    0.5,
    0.91,
    "Online Retail Dataset | December 2010 – December 2011",
    ha="center",
    fontsize=11
)

ax.set_xlabel("Month", fontsize=12, labelpad=12)
ax.set_ylabel("Revenue (£)", fontsize=12, labelpad=12)

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"£{x / 1000000:.1f}M"
    )
)

ax.tick_params(axis="x", rotation=45)

ax.text(
    0.99,
    0.02,
    "Note: December 2011 data ends on 9 December.",
    transform=ax.transAxes,
    ha="right",
    fontsize=9,
    color="dimgray"
)

ax.grid(True, alpha=0.25)

fig.subplots_adjust(
    top=0.83,
    bottom=0.15,
    left=0.10,
    right=0.97
)

fig.savefig(
    "monthly_revenue_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# =====================================
# 6. TOP 10 MERCHANDISE PRODUCTS
# =====================================

# Exclude postage and manual entries
excluded_products = ["POSTAGE", "MANUAL"]

merchandise = df_clean[
    ~df_clean["Description"].str.strip().str.upper().isin(
        excluded_products
    )
].copy()

top_merchandise = (
    merchandise.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(13, 7))

top_merchandise.sort_values().plot(
    kind="barh",
    ax=ax,
    edgecolor="black"
)

ax.set_title(
    "Top 10 Merchandise Products by Revenue",
    fontsize=18,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Revenue (£)", fontsize=12)
ax.set_ylabel("Product", fontsize=12)

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"£{x / 1000:,.0f}K"
    )
)

ax.grid(axis="x", alpha=0.25)

fig.tight_layout()

fig.savefig(
    "top_products_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# =====================================
# 7. TOP 10 COUNTRIES BY REVENUE
# =====================================

country_data = top_countries.sort_values(
    ascending=True
)

fig, ax = plt.subplots(figsize=(13, 7))

country_data.plot(
    kind="barh",
    ax=ax,
    edgecolor="black"
)

ax.set_title(
    "Top 10 Countries by Revenue",
    fontsize=18,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Revenue (£)", fontsize=12)
ax.set_ylabel("Country", fontsize=12)

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"£{x / 1000:,.0f}K"
    )
)

ax.grid(axis="x", alpha=0.25)

fig.tight_layout()

fig.savefig(
    "top_countries_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================
# 8. INTERNATIONAL REVENUE (EXCLUDING UK)
# =====================================

international_revenue = (
    df_clean[df_clean["Country"] != "United Kingdom"]
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(13, 7))

international_revenue.sort_values().plot(
    kind="barh",
    ax=ax,
    edgecolor="black"
)

ax.set_title(
    "Top 10 International Markets by Revenue (Excluding UK)",
    fontsize=18,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Revenue (£)", fontsize=12)
ax.set_ylabel("Country", fontsize=12)

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"£{x / 1000:,.0f}K"
    )
)

ax.grid(axis="x", alpha=0.25)

fig.tight_layout()

fig.savefig(
    "international_revenue_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nINTERNATIONAL REVENUE CHART GENERATED SUCCESSFULLY!")


# =====================================
# 8. COMPLETION MESSAGE
# =====================================

print("\n=====================================")
print("CUSTOMER ANALYSIS COMPLETED")
print("=====================================")

print("Monthly revenue chart generated.")
print("Top products chart generated.")
print("Top countries chart generated.")

print("\nAll charts saved successfully!")

# =====================================
# 9. CUSTOMER SEGMENTATION - RFM ANALYSIS
# =====================================

# Set analysis date
analysis_date = df_clean["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df_clean.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

print("\nRFM CUSTOMER ANALYSIS:")
print(rfm.head())

# Calculate RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

# Combine scores
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

print("\nCUSTOMER RFM SCORES:")
print(rfm.head(10))

print("\nRFM SUMMARY:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())

# =====================================
# 10. CUSTOMER SEGMENT CLASSIFICATION
# =====================================

def classify_customer(row):

    if row["R_Score"] >= 3 and row["F_Score"] >= 3 and row["M_Score"] >= 3:
        return "Champions"

    elif row["R_Score"] >= 3 and row["F_Score"] >= 2:
        return "Loyal Customers"

    elif row["R_Score"] >= 3 and row["F_Score"] <= 2:
        return "Potential Loyalists"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"

    elif row["R_Score"] == 1 and row["F_Score"] == 1:
        return "Lost Customers"

    else:
        return "Other Customers"


rfm["Segment"] = rfm.apply(classify_customer, axis=1)

# Count customers in each segment
segment_counts = rfm["Segment"].value_counts()

print("\nCUSTOMER SEGMENT DISTRIBUTION:")
print(segment_counts)

# Revenue by segment
segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY CUSTOMER SEGMENT:")
print(segment_revenue)

# Average spending by segment
segment_average = (
    rfm.groupby("Segment")["Monetary"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE CUSTOMER VALUE BY SEGMENT:")
print(segment_average)

# =====================================
# 11. CUSTOMER SEGMENT VISUALISATION
# =====================================

# Chart 1: Customer Distribution

fig, ax = plt.subplots(figsize=(12, 7))

segment_counts.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_title(
    "Customer Distribution by Segment",
    fontsize=18,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Number of Customers")
ax.set_ylabel("Customer Segment")

for container in ax.containers:
    ax.bar_label(container, padding=4)

fig.tight_layout()

fig.savefig(
    "customer_segment_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Chart 2: Revenue by Customer Segment

fig, ax = plt.subplots(figsize=(12, 7))

segment_revenue.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_title(
    "Revenue Contribution by Customer Segment",
    fontsize=18,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Revenue (£)")
ax.set_ylabel("Customer Segment")

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"£{x / 1000000:.1f}M"
    )
)

for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"£{v.get_width()/1000000:.2f}M" for v in container],
        padding=4,
        fontsize=9
    )

fig.tight_layout()

fig.savefig(
    "customer_segment_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCUSTOMER SEGMENT CHARTS GENERATED SUCCESSFULLY!")

# =====================================
# EXPORT DATASETS FOR POWER BI
# =====================================

# 1. Cleaned transaction dataset
df_clean.to_csv("cleaned_online_retail.csv", index=False)

# 2. Customer RFM and segmentation dataset
rfm.to_csv("customer_rfm_segments.csv", index=True)

# 3. Monthly revenue
monthly_revenue.rename("Revenue").to_csv("monthly_revenue.csv", header=True)

# 4. Country revenue
country_revenue = df_clean.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
country_revenue.to_csv("country_revenue.csv", header=True)

# 5. Product revenue
product_revenue = (
    df_clean.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
product_revenue.to_csv("product_revenue.csv", header=True)

print("\nALL DATASETS EXPORTED SUCCESSFULLY!")
