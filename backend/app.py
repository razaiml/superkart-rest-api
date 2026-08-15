
# Importing data manipulation libraries
import numpy as np
import pandas as pd

# Importing Model Serialization/Deseralization library
import joblib

# Importing Flask to create the Backend (API, requests, etc.)
from flask import Flask, request, jsonify

# Initializing the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Loading the trained machine learning model
model = joblib.load("superkart_prediction_model_v1_0.joblib")

# Defining a route for the home page (GET request)
@superkart_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API! We have cookies! 😉"

# Defining an endpoint for single store prediction (POST request)
@superkart_api.post('/v1/predict')
def predict_single_sale():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing store details and returns
    the predicted sale as a JSON response.
    """
    # Getting the JSON data from the request body
    store_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': store_data['Product_Weight'],
        'Product_Sugar_Content': store_data['Product_Sugar_Content'],
        'Product_Allocated_Area': store_data['Product_Allocated_Area'],
        'Product_MRP': store_data['Product_MRP'],
        'Store_Size': store_data['Store_Size'],
        'Store_Location_City_Type': store_data['Store_Location_City_Type'],
        'Store_Type': store_data['Store_Type']
    }

    # Converting the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Making predictions
    predicted_sale = model.predict(input_data)[0]

    # Returning the actual price
    return jsonify({'Sales (in USD)': predicted_sale})


# Defining an endpoint for batch prediction (POST request)
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing multiple store details and returns
    the predicted sales as two dictionaries in the JSON response:
         * one row per store dictionary
         * clusters of multiple stores grouped by Store_Type.
    """
    # Getting the uploaded CSV file from the request
    file = request.files['file']

    # Reading the CSV file into a Pandas DataFrame
    if "file" not in request.files:
        return {"error": "No CSV file provided"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "No file selected"}, 400

    input_data = pd.read_csv(file)

    # Clean column names
    input_data.columns = input_data.columns.str.strip()

    # Defining the expected columns as in the model
    feature_columns = [
        'Product_Weight',
        'Product_Sugar_Content',
        'Product_Allocated_Area',
        'Product_MRP',
        'Store_Size',
        'Store_Location_City_Type',
        'Store_Type']

    # Validate required columns
    missing = set(feature_columns) - set(input_data.columns)

    if missing:
        return {
            "error": "Missing columns.",
            "columns": sorted(missing)
        }, 400



    # Keep model features
    model_features = input_data[feature_columns]

    # Making predictions for all the stores in the DataFrame
    predicted_sales = model.predict(model_features)

    # Attaching predictions
    prediction_df = model_features.copy()
    prediction_df["Product_Store_Sales_Total"] = predicted_sales

    # Aggregating by Store_Type
    store_summary = (
        prediction_df
        .groupby("Store_Type", as_index=False)
        ["Product_Store_Sales_Total"]
        .sum()
        )

    # Returning the predictions dictionaries as a JSON response
    return {
        "row_predictions": prediction_df.to_dict(orient="records"),
        "store_summary": store_summary.to_dict(orient="records")
    }

# Running the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_api.run(debug=True)
