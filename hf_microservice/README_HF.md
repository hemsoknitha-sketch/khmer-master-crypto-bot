# Hugging Face Space Deployment Guide for `khmer-master-crypto-bot`

This directory contains the AI Super Brain Microservice for **APEX AGI ENGINE v11.0**.

## 🚀 Steps to Deploy on Hugging Face (100% Free):

1. Log in to [Hugging Face](https://huggingface.co/)
2. Click **New Space**
3. Set **Space Name**: `khmer-master-crypto-bot`
4. Choose **SDK**: `Docker` (Blank) or `FastAPI`
5. Set **License**: `mit`
6. Set **Visibility**: `Public` (or `Private` with HF Access Token)
7. Push files to your Space Git repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/khmer-master-crypto-bot
   cp -r hf_microservice/* khmer-master-crypto-bot/
   cd khmer-master-crypto-bot
   git add .
   git commit -m "Deploy APEX AGI Super Brain Microservice v11.0"
   git push origin main
   ```
8. Optional: Set Environment Variable `GEMINI_API_KEY` in Hugging Face Space **Settings -> Variables and secrets**.

## 🌐 Endpoint URLs:
- Base URL: `https://YOUR_HF_USERNAME-khmer-master-crypto-bot.hf.space`
- Health Ping: `/health`
- ML Prediction: `/predict`
- AI Market Analysis: `/analyze`
- News Sentiment: `/news`
