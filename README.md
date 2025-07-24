# 💡 AI-Powered Dynamic Pricing Engine

**Live Demo:** http://10.41.209.102:8501
## 🎯 Problem Statement

In e-commerce and retail, setting the right price for a product is a critical challenge. A price too high deters customers, while a price too low reduces potential revenue. This project demonstrates an end-to-end solution that uses machine learning to recommend the optimal price for a product on a given day to maximize revenue.

## ✨ Features

*   **Dynamic Price Recommendation:** Get an optimal price recommendation based on a selected date.
*   **Explainable AI (XAI):** An interactive Plotly chart shows the relationship between price and predicted revenue, explaining *why* the price is optimal.
*   **Full-Stack Implementation:** Covers the complete pipeline from data simulation and model training to a user-facing web app.
*   **Deployment-Ready:** The entire application is containerized with Docker for easy deployment and reproducibility.

## 🛠️ Tech Stack

*   **Modeling:** Python, Pandas, Scikit-learn, XGBoost
*   **Frontend:** Streamlit
*   **Data Visualization:** Plotly
*   **Containerization:** Docker

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hemanthDA/Dynamic-Price-Engine.git
    cd Dynamic-Price-Engine
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Train the model:**
    ```bash
    python app/core/model_training.py
    ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run app/main.py
    ```

workflow diagarm 
<img width="1024" height="1024" alt="82af35c8-f070-48f2-b1af-4fa55ed57985" src="https://github.com/user-attachments/assets/30b46491-8894-4396-b83b-8b80127e35e3" />


