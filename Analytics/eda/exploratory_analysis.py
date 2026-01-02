import os
import pandas as pd
import matplotlib.pyplot as plt
ROOT = "C:/Users/KIIT0001/Documents/CRO Project"
CLEAN_PATH = f"{ROOT}/data/processed/events_clean.csv"
OUTPUT_DIR = f"{ROOT}/outputs/eda"
os.makedirs(OUTPUT_DIR, exist_ok=True)
df = pd.read_csv(CLEAN_PATH)
print("Shape:", df.shape)
print("Columns:", list(df.columns))
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

print("\nEvent counts:")
event_counts = df["event"].value_counts()
print(event_counts)
plt.figure(figsize=(6, 4))
event_counts.plot(kind="bar")
plt.title("Event Type Distribution")
plt.xlabel("Event Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/event_distribution.png")
plt.close()


df["date"] = df["timestamp"].dt.date
daily = df.groupby("date").size()
daily.index = pd.to_datetime(daily.index)

full_range = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
daily = daily.reindex(full_range, fill_value=0)

plt.figure(figsize=(12, 5))
daily.plot()
plt.title("Events Over Time (Daily)")
plt.xlabel("Date")
plt.ylabel("Number of Events")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/events_over_time_daily.png")
plt.close()

rolling7 = daily.rolling(7, min_periods=1).mean()
plt.figure(figsize=(12, 5))
rolling7.plot()
plt.title("Events Over Time (7-Day Moving Average)")
plt.xlabel("Date")
plt.ylabel("Events (7D MA)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/events_over_time_7dma.png")
plt.close()

events_per_user = df.groupby("visitorid").size()

plt.figure(figsize=(7, 4))
plt.hist(events_per_user, bins=50, range=(0, 50))
plt.title("Distribution of Events per User (0–50)")
plt.xlabel("Events per User")
plt.ylabel("Number of Users")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/events_per_user_0_50.png")
plt.close()

plt.figure(figsize=(7, 4))
plt.hist(events_per_user, bins=100, log=True)
plt.title("Distribution of Events per User (Log Scale)")
plt.xlabel("Events per User")
plt.ylabel("Number of Users (log)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/events_per_user_log.png")
plt.close()

print("\nQuick stats on events per user:")
print(events_per_user.describe())

print(f"\nEDA plots saved to: {OUTPUT_DIR}")
