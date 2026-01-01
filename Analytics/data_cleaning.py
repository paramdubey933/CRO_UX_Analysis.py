import os
import pandas as pd
ROOT = "C:/Users/KIIT0001/Documents/CRO Project"
RAW_PATH = f"{ROOT}/data/raw/events.csv"            
PROCESSED_DIR = f"{ROOT}/data/processed"
PROCESSED_PATH = f"{PROCESSED_DIR}/events_clean.csv"

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Loading:", RAW_PATH)
df = pd.read_csv(RAW_PATH)

print("Initial shape:", df.shape)
print("Columns:", list(df.columns))

df = df.dropna(how="all")

expected = {"timestamp", "visitorid", "event", "itemid"}
missing = expected - set(df.columns)
if missing:
    raise ValueError(f"Columns missing from events.csv: {missing}")

df = df.drop_duplicates()
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
before = df.shape[0]
df = df.dropna(subset=["timestamp"])
after = df.shape[0]
print(f"Dropped rows with bad timestamp: {before - after}")

df = df.sort_values(["visitorid", "timestamp"]).reset_index(drop=True)
print("\nEvent distribution BEFORE saving:")
print(df["event"].value_counts(dropna=False))

df.to_csv(PROCESSED_PATH, index=False)
print(f"\n Saved cleaned data to: {PROCESSED_PATH}")
print("Final shape:", df.shape)
