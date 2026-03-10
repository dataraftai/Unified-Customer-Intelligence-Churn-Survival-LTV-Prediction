from pydantic import BaseModel ,Field

class ChurnAnalysis(BaseModel):
    predicted : int = Field(...,description="prediction for are customers are likely to be expensive",example=0)
    churn_label : str = Field(...,description="The predicted category for are customers are likely to be churn or not churn",example="Churn")
    churn_probability : float = Field(...,description="Confidance score for more like to be predicted (range 0 to 1) ")

class LTVAnalysis(BaseModel):
    prediction_lifetime_value: str = Field(..., example="$872.13")

# 3. Sub-model for Business Strategy
class BusinessSegment(BaseModel):
    non_profitable_segments: str = Field(..., example="No")
    priority: str = Field(..., example="Standard/High")

# 4. The Main Response Model
class PredictionResponce(BaseModel):
    churn_analysis: ChurnAnalysis
    ltv_analysis: LTVAnalysis
    business_segment: BusinessSegment