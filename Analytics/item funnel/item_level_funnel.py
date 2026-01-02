import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Step 0: Load cleaned data ---
data_path = r"C:/Users/KIIT0001/Documents/CRO Project/data/processed/events_clean.csv"
df = pd.read_csv(data_path)

# --- Step 1: Aggregate unique users per item per step ---
views = df[df["event"] == "view"].groupby("itemid")["visitorid"].nunique()
carts = df[df["event"] == "addtocart"].groupby("itemid")["visitorid"].nunique()
purchases = df[df["event"] == "transaction"].groupby("itemid")["visitorid"].nunique()

# --- Step 2: Combine into funnel dataframe ---
funnel_df = pd.DataFrame({
    "views": views,
    "add_to_cart_users": carts,
    "purchase_users": purchases
}).fillna(0)

# Conversion + Drop-off
funnel_df["view_to_cart"] = (funnel_df["add_to_cart_users"] / funnel_df["views"].replace(0, 1)).round(3)
funnel_df["cart_to_purchase"] = (funnel_df["purchase_users"] / funnel_df["add_to_cart_users"].replace(0, 1)).round(3)
funnel_df["view_to_purchase"] = (funnel_df["purchase_users"] / funnel_df["views"].replace(0, 1)).round(3)

# --- Step 3: Save outputs ---
output_dir = r"C:/Users/KIIT0001/Documents/CRO Project/outputs/item_funnel_full"
os.makedirs(output_dir, exist_ok=True)

funnel_df.to_csv(os.path.join(output_dir, "item_funnel_full.csv"))

# --- Step 4: Top items by engagement (views) ---
top_items = funnel_df.sort_values("views", ascending=False).head(20)

plt.figure(figsize=(12, 6))
top_items[["views", "add_to_cart_users", "purchase_users"]].plot(kind="bar")
plt.title("Top 20 Items: Views → Add-to-Cart → Purchases")
plt.xlabel("Item ID")
plt.ylabel("Unique Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top20_items_funnel.png"))
plt.close()

plt.figure(figsize=(12, 6))
top_items[["view_to_cart", "cart_to_purchase", "view_to_purchase"]].plot(kind="bar")
plt.title("Top 20 Items: Conversion Rates")
plt.xlabel("Item ID")
plt.ylabel("Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top20_items_conversion.png"))
plt.close()

# --- Step 5: Worst performers (many views, low conversion) ---
worst_items = funnel_df[funnel_df["views"] > 100].sort_values("view_to_purchase").head(20)

plt.figure(figsize=(12, 6))
worst_items[["views", "add_to_cart_users", "purchase_users"]].plot(kind="bar", color=["#9999ff", "#ffcc00", "#ff6666"])
plt.title("Worst 20 Items: High Views but Low Conversion")
plt.xlabel("Item ID")
plt.ylabel("Unique Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "worst20_items_funnel.png"))
plt.close()

print(f"✅ Item-level funnel (full) completed. Results saved in: {output_dir}")
