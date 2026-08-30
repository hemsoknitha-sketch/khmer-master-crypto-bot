# ==============================================================================
# APEX AGI SUPER BRAIN - HUGGING FACE CLOUD AUTO-TRAINER & SYNC PIPELINE
# ==============================================================================
# Executes automated 2-week ML & AGI model retraining on Hugging Face / GitHub Runners
# Uploads updated model weights (.pkl) & configurations to Hugging Face Model Hub
# ==============================================================================

import os
import sys
import time
import json
import glob
from datetime import datetime

# Import training pipeline
import train_model

try:
    from huggingface_hub import HfApi, hf_hub_download
except ImportError:
    print("⚠️ [HF TRAINER] huggingface_hub not installed. Installing...")
    os.system(f"{sys.executable} -m pip install huggingface_hub")
    from huggingface_hub import HfApi, hf_hub_download

HF_REPO_ID = os.getenv("HF_MODEL_REPO", "hemsinath/apex-ai-brain-models")
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

def run_cloud_training_and_upload():
    """
    1. Triggers Super Brain Machine Learning Training (XGBoost, HMM, LSTM, Genetic DEAP).
    2. Uploads trained .pkl weights and brain_config.json to Hugging Face Hub.
    """
    print("==========================================================")
    print("🚀 [HF AUTO-TRAINER] Starting 2-Week Super Brain Training Cycle...")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==========================================================")
    
    start_time = time.time()
    
    # 1. Execute Full Training
    try:
        train_model.train_super_brain()
        print("✅ [HF AUTO-TRAINER] Super Brain model training completed successfully.")
    except Exception as e:
        print(f"❌ [HF AUTO-TRAINER ERROR]: Model training failed: {e}")
        sys.exit(1)
        
    duration_min = round((time.time() - start_time) / 60, 2)
    print(f"⚡ Training completed in {duration_min} minutes.")
    
    # 2. Upload Artifacts to Hugging Face Hub
    if not HF_TOKEN:
        print("⚠️ [HF AUTO-TRAINER] HF_TOKEN is missing. Models saved locally only.")
        return False
        
    print(f"📦 [HF AUTO-TRAINER] Uploading trained models to Hugging Face Repo ({HF_REPO_ID})...")
    api = HfApi(token=HF_TOKEN)
    
    try:
        api.create_repo(repo_id=HF_REPO_ID, repo_type="model", exist_ok=True, private=True)
    except Exception as e:
        print(f"ℹ️ Repo notice: {e}")
        
    files_to_upload = [
        "brain_price.pkl",
        "brain_trend.pkl",
        "brain_vol.pkl",
        "brain_tp.pkl",
        "brain_dca.pkl",
        "brain_scaler.pkl",
        "brain_catboost.pkl",
        "brain_lightgbm.pkl",
        "brain_graph.pkl",
        "brain_patchtst.h5",
        "brain_ppo_policy.json",
        "brain_moe_router.pkl",
        "brain_tgat_graph.pkl",
        "brain_actor_critic_allocator.json",
        "brain_pinn_jump_diff.pkl",
        "brain_config.json"
    ]
    
    uploaded_count = 0
    for f in files_to_upload:
        if os.path.exists(f):
            try:
                api.upload_file(
                    path_or_fileobj=f,
                    path_in_repo=f,
                    repo_id=HF_REPO_ID,
                    repo_type="model"
                )
                print(f"  └─ 🟢 Uploaded {f} -> Hugging Face Hub ({HF_REPO_ID})")
                uploaded_count += 1
            except Exception as e:
                print(f"  └─ ❌ Failed to upload {f}: {e}")
                
    if uploaded_count > 0:
        print(f"🎉 [HF AUTO-TRAINER SUCCESS] Uploaded {uploaded_count}/{len(files_to_upload)} files to Hugging Face Model Hub!")
        return True
    return False

if __name__ == "__main__":
    run_cloud_training_and_upload()
