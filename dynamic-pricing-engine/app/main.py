 
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from core.predictor import PricePredictor

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic Pricing Engine",
    page_icon="💡",
    layout="wide"
)

# --- Load Model ---
# Use a singleton pattern to load the model only once
@st.cache_resource
def get_predictor():
    try:
        predictor = PricePredictor()
        return predictor
    except FileNotFoundError:
        st.error("Model file not found. Please ensure the model is trained and available.")
        st.stop()

predictor = get_predictor()

# --- App Title and Description ---
st.title("💡 AI-Powered Dynamic Pricing Engine")
st.markdown("""
This application demonstrates an end-to-end Machine Learning project.
Select a date below, and the AI will recommend the optimal price to maximize revenue for that day.
The model was trained on synthetic historical sales data, capturing trends like seasonality and price elasticity.
""")

# --- User Input ---
st.sidebar.header("Configuration")
selected_date = st.sidebar.date_input(
    "Select a Date for Price Optimization",
    date.today()
)

# --- Main Logic and Display ---
if st.sidebar.button("🚀 Recommend Price"):
    with st.spinner('Analyzing market data and crunching numbers...'):
        # Convert date to pandas timestamp
        selected_date_ts = pd.to_datetime(selected_date)

        # Get optimal price and analysis data
        optimal_price, max_revenue, analysis_df = predictor.find_optimal_price(selected_date_ts)

        st.subheader(f"Price Recommendation for {selected_date.strftime('%B %d, %Y')}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Optimal Price",
                value=f"₹{optimal_price:.2f}"
            )
        with col2:
            st.metric(
                label="Predicted Maximum Revenue",
                value=f"₹{max_revenue:,.2f}"
            )

        st.markdown("---")
        st.subheader("Price vs. Revenue Analysis")

        # --- Interactive Plot ---
        fig = px.line(
            analysis_df,
            x="Price",
            y="Predicted_Revenue",
            title="How Predicted Revenue Changes with Price",
            labels={'Price': 'Product Price (₹)', 'Predicted_Revenue': 'Predicted Revenue (₹)'}
        )
        # Add a vertical line and annotation for the optimal price
        fig.add_vline(x=optimal_price, line_width=3, line_dash="dash", line_color="green")
        fig.add_annotation(
            x=optimal_price,
            y=max_revenue,
            text=f"Optimal Point: ₹{optimal_price:.2f}",
            showarrow=True,
            arrowhead=1,
            yshift=10
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **How to interpret this chart:** The curve shows the predicted revenue for different price points. Our AI found the peak of this curve, which represents the price that balances high demand with a high profit margin, thus maximizing total revenue.
        """)

else:
    st.info("Select a date and click 'Recommend Price' to start.")