# Upload Model to Google Cloud Storage

The model file needs to be uploaded to Cloud Storage so it can be downloaded at runtime.

## Option 1: Using Google Cloud Console (Easiest)

1. **Go to Cloud Storage Console:**
   https://console.cloud.google.com/storage/browser?project=bookie-ai-dc1f8

2. **Create a bucket** (if it doesn't exist):
   - Click "CREATE BUCKET"
   - Name: `bookie-ai-dc1f8-models`
   - Location: `us-east5` (same as Cloud Run)
   - Click "CREATE"

3. **Upload the model file:**
   - Click on the bucket `bookie-ai-dc1f8-models`
   - Click "UPLOAD FILES"
   - Select `api/recommender/ml_model.joblib` (149MB file)
   - Wait for upload to complete
   - The file should be named `ml_model.joblib` in the bucket

## Option 2: Using gcloud CLI

If you have gcloud CLI installed:

```bash
# Create bucket
gcloud storage buckets create gs://bookie-ai-dc1f8-models \
  --project=bookie-ai-dc1f8 \
  --location=us-east5

# Upload model
gcloud storage cp api/recommender/ml_model.joblib \
  gs://bookie-ai-dc1f8-models/ml_model.joblib
```

## How It Works

The API will:
1. First try to load the model from the local file
2. If the file is a Git LFS pointer (< 1MB), it will automatically download from Cloud Storage
3. Cache the downloaded file for subsequent requests

This solves the Git LFS issue in Cloud Build!

