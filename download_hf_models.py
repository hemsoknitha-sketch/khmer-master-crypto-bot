import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "khmer-master-crypto-bot", ".env")
load_dotenv(env_path)

from huggingface_hub import HfApi, hf_hub_download, list_repo_files

HF_REPO_ID = os.getenv("HF_MODEL_REPO", "hemsinath/apex-ai-brain-models")
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

models_dir = os.path.join(os.path.dirname(__file__), "khmer-master-crypto-bot", "models")
os.makedirs(models_dir, exist_ok=True)

print(f"Connecting to Hugging Face Model Hub: {HF_REPO_ID} ...")
api = HfApi(token=HF_TOKEN)

try:
    all_files = list_repo_files(repo_id=HF_REPO_ID, repo_type="model", token=HF_TOKEN)
    print(f"Total files available on Hugging Face Hub: {len(all_files)}")
    
    downloaded = 0
    for f in all_files:
        if f.startswith("."):
            continue
        print(f"Downloading {f} ...")
        try:
            download_path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=f,
                token=HF_TOKEN,
                local_dir=models_dir,
                repo_type="model"
            )
            file_size = os.path.getsize(download_path)
            print(f"  [OK] {f} -> {download_path} ({file_size / 1024:.1f} KB)")
            downloaded += 1
        except Exception as e:
            print(f"  [FAIL] Could not download {f}: {e}")

    print(f"\nSuccessfully downloaded and synchronized {downloaded} files into {models_dir}")
except Exception as e:
    print("Error querying repo files:", e)
