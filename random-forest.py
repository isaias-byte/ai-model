# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt  # For plotting (currently unused)
import seaborn as sns            # For advanced plotting (currently unused)
from sklearn.ensemble import RandomForestClassifier # The specific algorithm we're using
from sklearn.model_selection import train_test_split  # Utility to split data

# Load the Data
file_path = "card_transdata.csv"
data = pd.read_csv(file_path)

# Prepare Data for Modeling
# Separate features (X) and the target variable (y)
# X contains all columns EXCEPT 'fraud' (these are the inputs)
x = data.drop("fraud", axis=1)
# y contains only the 'fraud' column (this is what we want to predict)
y = data["fraud"]

# Split the Data
# Divide the dataset into training (80%) and testing (20%) sets.
# The model will learn from the training set.
# We use the testing set to evaluate how well the model learned.
# random_state=42 ensures we get the same "random" split every time we run the code.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize and Train the Model
# Initialize the Random Forest Classifier.
# random_state=42 ensures the model's internal randomness is reproducible.
rf_classifier = RandomForestClassifier(random_state=42)

# Train (fit) the model using the training data (x_train, y_train).
# The model learns patterns linking the features (x_train) to the outcome (y_train).
rf_classifier.fit(x_train, y_train)

# --- (Optional Feature Importance Check) ---
# These lines (if uncommented) would show which features the model found most important.
# feature_importances = pd.Series(rf_classifier.feature_importances_, index=x.columns).sort_values(ascending=False)
# print("Ranked Feature Importance:")
# print(feature_importances)

# Test with a sample transaction (from existing data)
# This just demonstrates taking a random sample from the original data.
new_transaction_features = data.sample(1).drop("fraud", axis=1)
print("Randomly sampled features of new transaction")
print(new_transaction_features)

# Test with a new, manually defined transaction
# Create a new DataFrame representing one new transaction.
# The model has never seen this specific data point.
new_transaction_features1 = pd.DataFrame({
    'distance_from_home': [7],
    'distance_from_last_transaction': [3],
    'ratio_to_median_purchase_price': [0.1],
    'repeat_retailer': [0],
    'used_chip': [1],
    'used_pin_number': [0],
    'online_order': [0]
})

# Make a Prediction
# Use the trained model (.predict()) to predict the outcome for the new manual transaction.
prediction = rf_classifier.predict(new_transaction_features1)

# Display the Result
# The 'prediction' variable is an array (e.g., [0] or [1]).
# We check the first element (prediction[0]) to give a clean output.
print("Prediction for new transaction:")
print("Fraud" if prediction[0] == 1 else "Legitimate")