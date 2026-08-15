
# Importing data manipulation libraries
import pandas as pd

# Importing Streamlit to create the Frontend
import streamlit as st

# Importing HTTP requests to the deployed Flask API
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Predictor")

# Section for the single store prediction
st.subheader("Single Product/Store Online Prediction")

# Collecting user input for property features
Product_Weight = st.number_input("Product_Weight", min_value = 0.01, max_value = 50.00, value = 12.00)
Product_Sugar_Content= st.selectbox("Product_Sugar_Content", ["No Sugar", "Low Sugar", "Regular"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area", min_value= 0.001, max_value = 1.000,value = 0.060)
Product_MRP = st.number_input("Product_MRP", min_value = 0.01, max_value = 1000.00, value = 145.00)
Store_Size = st.selectbox("Store_Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store_Type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        predicted_sale = response.json()['Sales (in USD)']
        st.success(f"Predicted Product/Store Sales (in USD): {predicted_sale}")
    else:
        st.error("Unable to connect to the SuperKart Sales Prediction API! 😢")

# Section for batch prediction
st.subheader("Multiple Product/Store Batch Predictions")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the SuperKart Sales Prediction API! 😢")
