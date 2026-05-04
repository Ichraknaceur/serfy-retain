from __future__ import annotations


ID_COLUMN = "clientnum"
TARGET_COLUMN = "target"

CATEGORICAL_FEATURES = [
    "gender",
    "education_level",
    "marital_status",
    "income_category",
    "card_category",
]

NUMERICAL_FEATURES = [
    "customer_age",
    "dependent_count",
    "months_on_book",
    "total_relationship_count",
    "months_inactive_12_mon",
    "contacts_count_12_mon",
    "credit_limit",
    "total_revolving_bal",
    "avg_open_to_buy",
    "total_amt_chng_q4_q1",
    "total_trans_amt",
    "total_trans_ct",
    "total_ct_chng_q4_q1",
    "avg_utilization_ratio",
]

ENGINEERED_FEATURES = [
    "tenure_per_age",
    "utilization_per_age",
    "credit_limit_per_age",
    "total_trans_amt_per_credit_limit",
    "total_trans_ct_per_credit_limit",
]

MODEL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES + ENGINEERED_FEATURES

RAW_TO_CANONICAL_COLUMN_MAP = {
    "CLIENTNUM": ID_COLUMN,
    "Attrition_Flag": TARGET_COLUMN,
    "Customer_Age": "customer_age",
    "Gender": "gender",
    "Dependent_count": "dependent_count",
    "Education_Level": "education_level",
    "Marital_Status": "marital_status",
    "Income_Category": "income_category",
    "Card_Category": "card_category",
    "Months_on_book": "months_on_book",
    "Total_Relationship_Count": "total_relationship_count",
    "Months_Inactive_12_mon": "months_inactive_12_mon",
    "Contacts_Count_12_mon": "contacts_count_12_mon",
    "Credit_Limit": "credit_limit",
    "Total_Revolving_Bal": "total_revolving_bal",
    "Avg_Open_To_Buy": "avg_open_to_buy",
    "Total_Amt_Chng_Q4_Q1": "total_amt_chng_q4_q1",
    "Total_Trans_Amt": "total_trans_amt",
    "Total_Trans_Ct": "total_trans_ct",
    "Total_Ct_Chng_Q4_Q1": "total_ct_chng_q4_q1",
    "Avg_Utilization_Ratio": "avg_utilization_ratio",
}

TARGET_VALUE_MAP = {
    "Existing Customer": 0,
    "Attrited Customer": 1,
    "existing customer": 0,
    "attrited customer": 1,
    "0": 0,
    "1": 1,
    0: 0,
    1: 1,
}
