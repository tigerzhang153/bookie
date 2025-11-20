# Deploy API to Google Cloud Run

## Prerequisites
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project bookie-ai-dc1f8`

## Option 1: Deploy using gcloud CLI (Recommended - Easiest)

```bash
# From the project root directory
# Build and deploy to Cloud Run (gcloud will build the Docker image automatically)
gcloud run deploy bookie-api \
  --source api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300 \
  --max-instances 10
```

## Option 2: Deploy using Docker

```bash
# From the project root directory
# Build the Docker image (Dockerfile is in api/ directory)
docker build -t gcr.io/bookie-ai-dc1f8/bookie-api -f api/Dockerfile .

# Push to Google Container Registry
docker push gcr.io/bookie-ai-dc1f8/bookie-api

# Deploy to Cloud Run
gcloud run deploy bookie-api \
  --image gcr.io/bookie-ai-dc1f8/bookie-api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300
```

## After Deployment

1. Get the service URL:
```bash
gcloud run services describe bookie-api --region us-central1 --format 'value(status.url)'
```

2. Update `src/config.js` with the Cloud Run URL:
```javascript
const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://bookie-api-xxxxx-uc.a.run.app'  // Your Cloud Run URL
    : 'http://localhost:8000'
}
```

3. Test the health endpoint:
```bash
curl https://bookie-api-xxxxx-uc.a.run.app/health
```

## Important Notes

- The model file (149MB) will be included in the Docker image
- Cloud Run has a 10GB container size limit (you're well within this)
- Memory: Set to 2Gi to handle the model loading
- Timeout: Set to 300 seconds for model loading time
- The service will scale to zero when not in use (free tier friendly)

