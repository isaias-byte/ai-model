import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "card_transdata.csv"
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())

# Display the last rows of the dataset
print("\n", data.tail())

# Display the shape of the dataset
print("\n", data.info())

# Display the columns of the dataset
print("\n", data.shape)

# print("\n", data.describe())

# print("\n", data.dtypes)

missing_values = data.isnull().any(axis=1)
print("Rows with missing values:")
print(missing_values) 

duplicate_rows = data[data.duplicated()]
print("Duplicate rows:")
print(duplicate_rows)

# Clean the dataset by removing rows with missing values and duplicates
data.dropna(axis=0, inplace=True)
data.drop_duplicates(inplace=True)

# checking security of pin and chip transactions
chippindf = data[["used_chip", "used_pin_number", "fraud"]]
total_transactions = len(chippindf)
total_fraud = chippindf["fraud"].sum()
fraud_by_chip = chippindf[chippindf["used_chip"] == 1]["fraud"].sum()
fraud_by_pin = chippindf[chippindf["used_pin_number"] == 1]["fraud"].sum()

print("\n\nTotal Transactions:", total_transactions)
print("Total fraud cases:", total_fraud)
print(f"Fraud cases using chip: {fraud_by_chip} out of {total_transactions}")
print(f"Fraud cases using pin number: {fraud_by_pin} out of {total_transactions}")

# Optional: Set a nice Seaborn theme
sns.set(style="whitegrid")

# Define colors and labels
labels = ["Non-Fraud", "Fraud"]
chip_sizes = [total_transactions - fraud_by_chip, fraud_by_chip]
pin_sizes = [total_transactions - fraud_by_pin, fraud_by_pin]
colors = ["#4DB6AC", "#FF7043"]  # Teal and Coral

# Create subplots
plt.figure(figsize=(14, 7))

# Pie Chart: Chip
plt.subplot(1, 2, 1)
plt.pie(
    chip_sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    startangle=140,
    textprops={'fontsize': 12}
)
plt.axis("equal")
plt.title("Fraud in Chip Transactions", fontsize=14, fontweight='bold')

# Pie Chart: PIN
plt.subplot(1, 2, 2)
plt.pie(
    pin_sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    startangle=140,
    textprops={'fontsize': 12}
)
plt.axis("equal")
plt.title("Fraud in PIN Transactions", fontsize=14, fontweight='bold')

# Main Title
plt.suptitle("Fraud Cases: Chip vs PIN Usage", fontsize=16, fontweight='bold')

plt.tight_layout(pad=3.0)
plt.show()


# Correlation between transaction amount and fraud
# Calculate correlation
correlation_df = data[["ratio_to_median_purchase_price", "fraud"]]
correlation = correlation_df["ratio_to_median_purchase_price"].corr(correlation_df["fraud"])
print(f"\n\nCorrelation between transaction amount and fraud: {correlation:.4f}")

# Calculate averages
avg_non_fraud_transactions = correlation_df[correlation_df["fraud"] == 0]["ratio_to_median_purchase_price"].mean()
avg_fraud_transactions = correlation_df[correlation_df["fraud"] == 1]["ratio_to_median_purchase_price"].mean()

print(f"Average ratio to median purchase price for non fraudulent transactions: {avg_non_fraud_transactions:.4f}")
print(f"Average ratio to median purchase price for fraudulent transactions: {avg_fraud_transactions:.4f}")

# Plot settings
categories = ["Non-Fraudulent", "Fraudulent"]
average_ratio = [avg_non_fraud_transactions, avg_fraud_transactions]
colors = ["#4DB6AC", "#FF7043"]  # Teal for non-fraud, Coral for fraud

# Create bar plot
plt.figure(figsize=(8, 6))
bars = plt.bar(categories, average_ratio, color=colors, edgecolor='black')

# Add value labels above bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.05,
        f"{height:.2f}",
        ha='center',
        fontsize=12,
        fontweight='bold'
    )

# Plot formatting
plt.title("Average Ratio to Median Purchase Price by Transaction Type", fontsize=14, fontweight='bold')
plt.xlabel("Transaction Category", fontsize=12)
plt.ylabel("Avg. Ratio to Median Purchase Price", fontsize=12)
plt.ylim(0, max(average_ratio) + 1.5)
plt.tight_layout()

# Show plot
plt.show()


# Checking fraud cases in online transactions
online_order_df = data[["online_order", "fraud"]]
total_online_orders = online_order_df["online_order"].sum()
total_online_fraud = online_order_df[(online_order_df["fraud"] == 1) & (online_order_df["online_order"] == 1)]["fraud"].count()
fraud_rate_online = total_online_fraud / total_online_orders

total_offline_orders = len(online_order_df) - total_online_orders
total_offline_fraud = online_order_df[(online_order_df["fraud"] == 1) & (online_order_df["online_order"] == 0)]["fraud"].count()
fraud_rate_offline = total_offline_fraud / total_offline_orders
print(f"\n\nFraud rate for online transactions: {fraud_rate_online:.2%} ({total_online_fraud} cases out of "
      f"{total_online_orders} online transactions)")
print(f"Fraud rate for offline transactions: {fraud_rate_offline:.2%} ({total_offline_fraud} cases out of "
      f"{total_offline_orders} offline transactions)")