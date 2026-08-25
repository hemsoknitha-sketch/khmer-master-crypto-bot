# ==============================================================================
# APEX AGI SUPER BRAIN - GOOGLE COLAB MASTER GPU TRAINER & HF HUB PIPELINE
# ==============================================================================
# Run this script directly inside Google Colab (Free T4 GPU / A100 GPU)
# Trains 5-Model Ensemble & pushes trained weights to Hugging Face Hub (0% VPS Load)
# ==============================================================================

# STEP 1: Install Dependencies inside Colab
# !pip install -q pandas numpy scikit-learn xgboost tensorflow hmmlearn yfinance requests joblib huggingface_hub deap causal-learn

import os
import sys
import time
import json
import requests
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

# Set your Hugging Face Access Token here (or via Colab Secrets)
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_REPO_ID = "hemsinath/apex-ai-brain-models"

print("==================================================================")
print("🚀 APEX AGI SUPER BRAIN - GOOGLE COLAB HIGH-SPEED GPU TRAINER")
print("==================================================================")

# Execute Full Training Pipeline
import train_model

print("🧠 [COLAB GPU] Starting 4-Year Deep Machine Learning & Neural Network Training...")
train_model.train_super_brain()

print("\n📦 [COLAB GPU] Uploading trained models to Hugging Face Model Hub...")
try:
    from huggingface_hub import HfApi
    api = HfApi(token=HF_TOKEN)
    api.create_repo(repo_id=HF_REPO_ID, repo_type="model", exist_ok=True, private=True)
    
    files_to_upload = [
        "brain_price.pkl",
        "brain_trend.pkl",
        "brain_vol.pkl",
        "brain_tp.pkl",
        "brain_dca.pkl",
        "brain_scaler.pkl",
        "brain_config.json"
    ]
    
    for f in files_to_upload:
        if os.path.exists(f):
            api.upload_file(
                path_or_fileobj=f,
                path_in_repo=f,
                repo_id=HF_REPO_ID,
                repo_type="model"
            )
            print(f"  └─ 🟢 Successfully uploaded {f} -> Hugging Face Hub ({HF_REPO_ID})")
            
    print("\n🎉 [COLAB GPU SUCCESS] All Model Weights Published to Hugging Face Cloud Model Hub!")
    print("👉 Now on Telegram, run /sync_brain to hot-update your Google Cloud VPS with 0% downtime!")
except Exception as e:
    print(f"❌ Upload error: {e}")
