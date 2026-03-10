from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input_pydantic import UserInput,COLUMN_MAPPING
from schema.prediction_responce import PredictionResponce 
from model.predict import MODEL_VERSION,model,ltv_model

import numpy as np
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Customer Churn Prediction API",
        "description": "Predicts Churn Risk and Customer Lifetime Value (LTV)",
        "endpoints": {
            "/predict": "Churn prediction endpoint",
            "/docs": "Swagger documentation"
            }
    }

@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "version" : MODEL_VERSION,
        "model_loaded" : model is not None
    }

@app.post("/predict",response_model=PredictionResponce)
def predict_churn(data:UserInput):

    input_df = pd.DataFrame([data.model_dump()])   
    input_df.rename(columns=COLUMN_MAPPING, inplace=True)
    
    try :

        # model1 churn_model (classification model)
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        # model2 ltv(regression model)

        ltv_input = input_df.drop(columns=["Total Charges", "Tenure"], errors='ignore')
        ltv_pred = float(ltv_model.predict(ltv_input)[0])
        
        # BUSINESS LOGIC: PROFITABILITY
        is_non_profit = "Yes" if (prediction == 1 and ltv_pred < 500) else "No"

        return JSONResponse(status_code=200,content={
        "churn_analysis": {
            "predicted":int(prediction),
            "churn_label" : "Churn" if prediction == 1 else "No Churn",
            "churn_probability":round(float(prob),4)
        },
        "ltv_analysis":{
            "prediction_lifetime_value": f"${round(ltv_pred,2)}"
        },
        "business_segment":{
            "non_profitable_segments": is_non_profit,
            "priority":"Low" if is_non_profit == "Yes" else "Standard/Hight"
        }

        })
    
    except Exception as e:

        return JSONResponse(status_code=500,content=str(e))