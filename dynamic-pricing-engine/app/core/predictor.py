import xgboost as xgb
import pandas as pd
import numpy as np
import os

class PricePredictor:
    """
    A class to load the trained model and find the optimal price.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            # Construct the default path relative to this script's location
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(base_dir, '..', 'model', 'xgb_pricer.json')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run model_training.py first.")

        self.model = xgb.XGBRegressor()
        self.model.load_model(model_path)
        print("Model loaded successfully.")

    def _create_features_for_date(self, date: pd.Timestamp, prices: np.ndarray) -> pd.DataFrame:
        """Creates a DataFrame with all necessary features for prediction."""
        df = pd.DataFrame({'price': prices})
        df['day_of_week'] = date.dayofweek
        df['month'] = date.month
        df['day_of_year'] = date.dayofyear
        df['year'] = date.year
        return df[['price', 'day_of_week', 'month', 'day_of_year', 'year']]

    def find_optimal_price(self, date: pd.Timestamp):
        """
        Calculates the optimal price for a given date by simulating a range of prices.

        Returns:
            A tuple containing:
            - The optimal price (float)
            - The predicted revenue at that price (float)
            - A DataFrame with the price vs. revenue analysis (for plotting)
        """
        # Simulate a range of potential prices
        possible_prices = np.linspace(50, 200, 151) # Test 151 prices from $50 to $200

        # Create features for each potential price
        features_df = self._create_features_for_date(date, possible_prices)

        # Predict units sold for each price
        predicted_units = self.model.predict(features_df)
        predicted_units = np.maximum(0, predicted_units) # Ensure non-negative predictions

        # Calculate revenue for each price
        revenue = possible_prices * predicted_units

        # Create a results DataFrame for analysis
        analysis_df = pd.DataFrame({
            'Price': possible_prices,
            'Predicted_Units_Sold': predicted_units,
            'Predicted_Revenue': revenue
        })

        # Find the price that maximizes revenue
        optimal_idx = analysis_df['Predicted_Revenue'].idxmax()
        optimal_price_row = analysis_df.loc[optimal_idx]

        optimal_price = optimal_price_row['Price']
        max_revenue = optimal_price_row['Predicted_Revenue']

        return optimal_price, max_revenue, analysis_df
