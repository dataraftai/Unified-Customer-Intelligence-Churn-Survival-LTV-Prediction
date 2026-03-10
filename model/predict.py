import pandas as pd
import joblib

with open ("model/costomer_churn_pipline.pkl","rb") as f:
    model = joblib.load(f)

with open ("model/ltv_model.pkl","rb") as f:
    ltv_model = joblib.load(f)

MODEL_VERSION = "1.0.0"
