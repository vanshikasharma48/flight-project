# ==========================================
# Flight Delay Analytics - Python Analysis
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================
# Define project paths
# ==============================

BASE_PATH = r"D:\datascienece_journey\flight-delay-analytics"

DATA_PATH = os.path.join(BASE_PATH, "data", "flights.csv")
OUTPUT_PATH = os.path.join(BASE_PATH, "outputs", "charts")
CLEAN_DATA_PATH = os.path.join(BASE_PATH, "data", "flights_cleaned.csv")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ==============================
# 1. Load Dataset
# ==============================

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nData Types:")
print(df.dtypes)

df.columns = df.columns.str.lower()

# ==============================
# 2. Data Cleaning
# ==============================

df = df[df['cancelled'] == 0]
df = df[df['diverted'] == 0]

df = df.dropna(subset=['arr_delay', 'dep_delay'])

print("\nDataset Shape After Cleaning:", df.shape)

# ==============================
# 3. Feature Engineering
# ==============================

df['total_delay'] = df['arr_delay'] + df['dep_delay']

df['dep_hour'] = (df['dep_time'] // 100).fillna(0)

def delay_category(delay):
    if delay <= 0:
        return "On Time"
    elif delay <= 30:
        return "Minor Delay"
    elif delay <= 60:
        return "Moderate Delay"
    else:
        return "Severe Delay"

df['delay_category'] = df['total_delay'].apply(delay_category)

def flight_period(hour):
    if 6 <= hour <= 10:
        return "Morning Peak"
    elif 16 <= hour <= 20:
        return "Evening Peak"
    else:
        return "Off Peak"

df['flight_period'] = df['dep_hour'].apply(flight_period)

# ==============================
# 4. Average Delay by Airline
# ==============================

delay_airline = df.groupby('airline')['total_delay'].mean().sort_values()

plt.figure(figsize=(10,5))
delay_airline.plot(kind='bar')
plt.title("Average Delay by Airline")
plt.ylabel("Average Delay (Minutes)")
plt.xlabel("Airline")
plt.savefig(os.path.join(OUTPUT_PATH, "airline_delay.png"))
plt.show()

# ==============================
# 5. Delay Trend by Month
# ==============================

df['month'] = pd.to_datetime(df['fl_date'], dayfirst=True, errors='coerce').dt.month

delay_month = df.groupby('month')['total_delay'].mean()

plt.figure(figsize=(10,5))
sns.lineplot(x=delay_month.index, y=delay_month.values)
plt.title("Average Delay by Month")
plt.xlabel("Month")
plt.ylabel("Average Delay")
plt.savefig(os.path.join(OUTPUT_PATH, "month_delay.png"))
plt.show()

# ==============================
# 6. Delay Distribution
# ==============================

plt.figure(figsize=(10,5))
sns.histplot(df['total_delay'], bins=50)
plt.title("Flight Delay Distribution")
plt.savefig(os.path.join(OUTPUT_PATH, "delay_distribution.png"))
plt.show()

# ==============================
# 7. Departure vs Arrival Delay
# ==============================

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='dep_delay', y='arr_delay', alpha=0.3)
plt.title("Departure Delay vs Arrival Delay")
plt.savefig(os.path.join(OUTPUT_PATH, "dep_vs_arr_delay.png"))
plt.show()

# ==============================
# 8. Top 10 Most Delayed Routes
# ==============================

df['route'] = df['origin'] + " → " + df['dest']

top_routes = df.groupby('route')['total_delay'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_routes.values, y=top_routes.index)
plt.title("Top 10 Most Delayed Routes")
plt.xlabel("Average Delay")
plt.savefig(os.path.join(OUTPUT_PATH, "top_routes_delay.png"))
plt.show()

# ==============================
# 9. Airport Delay Analysis
# ==============================

airport_delay = df.groupby('origin')['total_delay'].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
airport_delay.head(10).plot(kind='bar')
plt.title("Airports with Highest Average Delay")
plt.savefig(os.path.join(OUTPUT_PATH, "airport_delay.png"))
plt.show()

# ==============================
# 10. Delay Cause Analysis
# ==============================

delay_causes = df[
    ['delay_due_carrier','delay_due_weather','delay_due_nas','delay_due_security','delay_due_late_aircraft']
].mean()

plt.figure(figsize=(10,5))
delay_causes.plot(kind='bar')
plt.title("Average Delay by Cause")
plt.savefig(os.path.join(OUTPUT_PATH, "delay_causes.png"))
plt.show()

# ==============================
# 11. Correlation Heatmap
# ==============================

corr = df[['arr_delay','dep_delay','total_delay','distance','air_time']].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.savefig(os.path.join(OUTPUT_PATH, "correlation_heatmap.png"))
plt.show()

# ==============================
# 12. Save Clean Dataset
# ==============================

df.to_csv(CLEAN_DATA_PATH, index=False)

print("\nClean dataset saved for Power BI.")

# ==============================
# 13. Statistics Analysis
# ==============================

print("\n========== STATISTICS SUMMARY ==========")

stats = df[['arr_delay','dep_delay','total_delay','distance']].describe()
print(stats)

# Mean
mean_delay = df['total_delay'].mean()
print("\nAverage Total Delay:", mean_delay)

# Median
median_delay = df['total_delay'].median()
print("Median Delay:", median_delay)

# Variance
variance_delay = df['total_delay'].var()
print("Variance of Delay:", variance_delay)

# Correlation
correlation = df[['arr_delay','dep_delay','distance','air_time']].corr()

print("\nCorrelation Matrix:")
print(correlation)

plt.figure(figsize=(8,6))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap (Statistics)")
plt.show()

# ==============================
# Probability of Severe Delay
# ==============================

severe_delay = df[df['total_delay'] > 60]

probability = len(severe_delay) / len(df)

print("\nProbability of Severe Delay:", probability)

# ==============================
# Delay Distribution (Stats)
# ==============================

plt.figure(figsize=(8,5))
sns.histplot(df['total_delay'], bins=40)
plt.title("Delay Distribution")
plt.show()

# ==============================
# Outlier Detection (IQR)
# ==============================

q1 = df['total_delay'].quantile(0.25)
q3 = df['total_delay'].quantile(0.75)

iqr = q3 - q1

outliers = df[
    (df['total_delay'] < (q1 - 1.5 * iqr)) |
    (df['total_delay'] > (q3 + 1.5 * iqr))
]

print("\nQ1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Number of Outliers:", len(outliers))