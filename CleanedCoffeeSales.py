import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/SABIC-Recreation/Downloads/archive (1)/dirty_cafe_sales.csv")
df.replace(["ERROR", "UNKNOWN", ""],np.nan,inplace=True)
numeric_cols = ["Quantity","Price Per Unit","Total Spent"]

for col in numeric_cols:df[col] = pd.to_numeric(df[col], errors="coerce")

df["Transaction Date"] = pd.to_datetime(df["Transaction Date"],errors="coerce")

df.drop_duplicates(inplace=True)
mask = (df["Total Spent"].isna() &df["Quantity"].notna() &df["Price Per Unit"].notna())
df.loc[mask, "Total Spent"] = (df.loc[mask, "Quantity"] *df.loc[mask, "Price Per Unit"])
mask = (df["Quantity"].isna() &df["Total Spent"].notna() &df["Price Per Unit"].notna())

df.loc[mask, "Quantity"] = (df.loc[mask, "Total Spent"] /df.loc[mask, "Price Per Unit"])
mask = (df["Price Per Unit"].isna() &df["Total Spent"].notna() &df["Quantity"].notna())

df.loc[mask, "Price Per Unit"] = (df.loc[mask, "Total Spent"] /df.loc[mask, "Quantity"])

for col in numeric_cols:df[col].fillna(df[col].median(),inplace=True)

categorical_cols = ["Item","Payment Method","Location"]

for col in categorical_cols:df[col].fillna(df[col].mode()[0],inplace=True)

df["Transaction Date"].fillna(df["Transaction Date"].mode()[0],inplace=True)


for col in categorical_cols:
    df[col] = df[col].str.title()

df.to_csv("cleaned_cafe_sales.csv",index=False)

print("\n===== CAFE SALES REPORT =====\n")

print("Total Transactions :", len(df))
print("Total Revenue      :", round(df["Total Spent"].sum(), 2))
print("Average Order Value:", round(df["Total Spent"].mean(), 2))

print("\nMost Sold Item:")
print(df["Item"].value_counts().head(1))

print("\nMost Used Payment Method:")
print(df["Payment Method"].value_counts().head(1))

print("\nSales By Location:")
print(df.groupby("Location")["Total Spent"].sum())

print("\nCleaned dataset saved as 'cleaned_cafe_sales.csv'")
