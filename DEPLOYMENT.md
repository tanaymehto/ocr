# Deployment Guide - Google Cloud Run

## Prerequisites
1. Google Cloud account with billing enabled
2. gcloud CLI installed: https://cloud.google.com/sdk/docs/install
3. Docker Desktop installed (optional for local testing)

## Deployment Steps

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
```

### 2. Set Your Project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### 3. Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable vision.googleapis.com
```

### 4. Deploy to Cloud Run
```bash
gcloud run deploy ocr-web-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300
```

### 5. View Your App
After deployment, Cloud Run will provide a URL like:
```
https://ocr-web-app-xxxxx-uc.a.run.app
```

## Notes
- The service account credentials are automatically handled by Cloud Run
- No need to set GOOGLE_APPLICATION_CREDENTIALS environment variable
- The app will scale automatically based on traffic
- You only pay for the time your app is processing requests

## Cost Estimate
- Free tier: 2 million requests/month
- After free tier: ~$0.40 per million requests
- Vision API: First 1000 units/month free, then $1.50 per 1000 units

## For Internship Demo
Simply share the Cloud Run URL with your interviewer!
