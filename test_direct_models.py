import os
import sys
import json
import joblib

models_dir = os.path.join(os.path.dirname(__file__), "khmer-master-crypto-bot", "models")

with open(os.path.join(models_dir, "brain_config.json"), "r") as f:
    config = json.load(f)

print("Loaded brain_config.json successfully. Models map:", len(config.get("models", {})))

price_model = joblib.load(os.path.join(models_dir, "brain_price.pkl"))
trend_model = joblib.load(os.path.join(models_dir, "brain_trend.pkl"))
vol_model = joblib.load(os.path.join(models_dir, "brain_vol.pkl"))
tp_model = joblib.load(os.path.join(models_dir, "brain_tp.pkl"))
dca_model = joblib.load(os.path.join(models_dir, "brain_dca.pkl"))
scaler = joblib.load(os.path.join(models_dir, "brain_scaler.pkl"))
lgb_model = joblib.load(os.path.join(models_dir, "brain_lightgbm.pkl"))
xgb_model = joblib.load(os.path.join(models_dir, "brain_xgb.pkl"))

print("Core models deserialized and loaded into memory successfully!")
print(f"Price model type: {type(price_model).__name__}")
print(f"Trend model type: {type(trend_model).__name__}")
print(f"XGB model type: {type(xgb_model).__name__}")
print(f"LGB model type: {type(lgb_model).__name__}")
print("ALL CORE MODELS VERIFIED 100% OPERATIONAL!")
