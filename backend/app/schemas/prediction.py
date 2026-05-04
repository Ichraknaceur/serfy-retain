from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    customer_age: int = Field(..., ge=18, le=120)
    gender: str
    dependent_count: int = Field(..., ge=0)
    education_level: str
    marital_status: str
    income_category: str
    card_category: str
    months_on_book: int = Field(..., ge=0)
    total_relationship_count: int = Field(..., ge=0)
    months_inactive_12_mon: int = Field(..., ge=0)
    contacts_count_12_mon: int = Field(..., ge=0)
    credit_limit: float = Field(..., ge=0)
    total_revolving_bal: float = Field(..., ge=0)
    avg_open_to_buy: float = Field(..., ge=0)
    total_amt_chng_q4_q1: float
    total_trans_amt: float = Field(..., ge=0)
    total_trans_ct: int = Field(..., ge=0)
    total_ct_chng_q4_q1: float
    avg_utilization_ratio: float = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    churn_probability: float
    risk_level: str
    predicted_class: int
    model_name: str


class ModelInfoResponse(BaseModel):
    model_name: str
    target: str
    categorical_features: list[str]
    numerical_features: list[str]
    engineered_features: list[str]
    model_features: list[str]
    transformed_feature_count: int
    metrics: dict[str, float]
    artifacts_dir: str
