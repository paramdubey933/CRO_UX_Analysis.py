import pandas as pd
import matplotlib.pyplot as plt
import os


df = pd.read_csv("C:/Users/KIIT0001/Documents/CRO Project/data/processed/events_clean.csv")


df["timestamp"] = pd.to_datetime(df["timestamp"])


df = df.sort_values(by=["visitorid", "timestamp"])


session_gap = pd.Timedelta(minutes=30)


df["prev_time"] = df.groupby("visitorid")["timestamp"].shift()
df["time_diff"] = df["timestamp"] - df["prev_time"]


df["new_session"] = (df["time_diff"] > session_gap) | (df["time_diff"].isna())
df["session_id"] = df.groupby("visitorid")["new_session"].cumsum()

df = df.drop(columns=["prev_time", "time_diff", "new_session"])


session_stats = df.groupby(["visitorid", "session_id"]).agg(
    start_time=("timestamp", "min"),
    end_time=("timestamp", "max"),
    num_events=("event", "count"),
    unique_items=("itemid", "nunique"),
    had_transaction=("transactionid", lambda x: x.notna().any())
).reset_index()


session_stats["duration_min"] = (session_stats["end_time"] - session_stats["start_time"]).dt.total_seconds() / 60


output_folder = "C:/Users/KIIT0001/Documents/CRO Project/outputs/session_analysis"
os.makedirs(output_folder, exist_ok=True)


session_stats.to_csv(os.path.join(output_folder, "session_stats.csv"), index=False)


plt.figure(figsize=(6,4))
plt.hist(session_stats["num_events"], bins=50)
plt.title("Events per Session")
plt.xlabel("Number of Events")
plt.ylabel("Sessions")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "events_per_session.png"))
plt.close()


plt.figure(figsize=(6,4))
plt.hist(session_stats["duration_min"], bins=50, range=(0,60))  # cap at 60 min
plt.title("Session Duration Distribution (0-60 min)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Sessions")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "session_duration.png"))
plt.close()


conv_by_events = session_stats.groupby("num_events")["had_transaction"].mean()
plt.figure(figsize=(6,4))
conv_by_events.plot()
plt.title("Conversion Rate by Events per Session")
plt.xlabel("Number of Events in Session")
plt.ylabel("Conversion Rate")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "conversion_by_events.png"))
plt.close()


bins = [0, 5, 10, 20, 50, 100, 200, session_stats["num_events"].max()]
labels = ["1-5", "6-10", "11-20", "21-50", "51-100", "101-200", "200+"]


session_stats["event_bin"] = pd.cut(session_stats["num_events"], bins=bins, labels=labels, right=True)


conv_by_bin = session_stats.groupby("event_bin")["had_transaction"].mean()

plt.figure(figsize=(6,4))
conv_by_bin.plot(marker="o")
plt.title("Conversion Rate by Session Size (Binned)")
plt.xlabel("Events per Session (bins)")
plt.ylabel("Conversion Rate")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "conversion_by_events_binned.png"))
plt.close()

print("✅ Session-based analysis completed. Outputs saved in:", output_folder)

