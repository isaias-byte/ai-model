import pandas as pd

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