import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os

print("Starting model training script...")

# --- 1. Synthetic Data Generation ---
# We create a dataset that mimics real-world sales behavior.
# This version includes a more realistic price elasticity model.
np.random.seed(42)
num_days = 365 * 2  # Two years of data
dates = pd.to_datetime(pd.date_range(start='2022-01-01', periods=num_days))

# Simulate price fluctuations around a base price
base_price = 100
price_fluctuations = np.random.uniform(-30, 30, num_days)
prices = base_price + price_fluctuations

# --- MORE REALISTIC DEMAND MODEL (Price Elasticity) ---
# Base demand + seasonality (e.g., higher sales on weekends and in December)
base_demand = 80
# Weekend effect: 1.5x to 2.0x more sales
day_of_week_effect = np.array([1.0, 1.0, 1.0, 1.0, 1.2, 1.8, 1.6])[dates.dayofweek]
# Holiday effect: 2.5x to 3.5x more sales in December
month_effect = np.where(dates.month == 12, np.random.uniform(2.5, 3.5, num_days), 1.0)

# The core relationship: demand drops exponentially as price increases
# This creates a realistic "inverted U" revenue curve.
price_elasticity_factor = 2.5
demand = (base_demand * np.exp(-price_elasticity_factor * (prices - base_price) / base_price))
demand *= day_of_week_effect
demand *= month_effect
demand += np.random.normal(0, 5, num_days) # Add some random noise

# Ensure demand is non-negative and integer
demand = np.maximum(0, demand).astype(int)

df = pd.DataFrame({
    'date': dates,
    'price': prices,
    'units_sold': demand
})

print("Synthetic data generated with improved elasticity. Sample:")
print(df.head())
print("\nData Description:")
print(df.describe())

# --- 2. Feature Engineering ---
# The model needs numerical features, not just dates.
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['day_of_year'] = df['date'].dt.dayofyear
df['year'] = df['date'].dt.year

# Define features (X) and target (y)
features = ['price', 'day_of_week', 'month', 'day_of_year', 'year']
target = 'units_sold'

X = df[features]
y = df[target]

# --- 3. Model Training ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Using XGBoost, a powerful gradient boosting model
# These hyperparameters are a good starting point
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=6,
    subsample=0.7,
    colsample_bytree=0.7,
    random_state=42,
    n_jobs=-1 # Use all available CPU cores
)

print("\nTraining XGBoost model...")
# Use early stopping to prevent overfitting and find the optimal number of trees
model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    early_stopping_rounds=50,
    verbose=False
)

# --- 4. Saving the Model ---
# Ensure the model directory exists
# This makes the script runnable from any location
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, '..', 'model')
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'xgb_pricer.json')
model.save_model(model_path)

print(f"\nModel trained and saved successfully to {model_path}")