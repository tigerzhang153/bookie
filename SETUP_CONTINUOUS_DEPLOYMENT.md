# Set Up Cloud Run Continuous Deployment

## Option 1: Set Up Continuous Deployment (Recommended)

1. **Go to Cloud Run Console:**
   https://console.cloud.google.com/run?project=bookie-ai-dc1f8

2. **Click on your `bookie` service**

3. **Click "EDIT & DEPLOY NEW REVISION"**

4. **Go to "Continuous deployment" section** (at the bottom of the page)

5. **Click "SET UP CONTINUOUS DEPLOYMENT"**

6. **Configure:**
   - **Source**: Select "Cloud Source Repositories" or "GitHub"
   - **Repository**: `tigerzhang153/bookie`
   - **Branch**: `main`
   - **Build type**: Dockerfile
   - **Dockerfile location**: `Dockerfile` (if building from root) OR `api/Dockerfile` (if building from api)
   - **Docker context**: `.` (root) OR `api` (if using api directory)

7. **Click "SAVE"**

## Option 2: Manual One-Time Deployment

If you want to deploy manually without continuous deployment:

1. **Go to Cloud Build:**
   https://console.cloud.google.com/cloud-build/builds?project=bookie-ai-dc1f8

2. **Click "TRIGGERS"**

3. **Click "CREATE TRIGGER"**

4. **Configure:**
   - **Name**: `bookie-api-deploy`
   - **Event**: Push to a branch
   - **Source**: Connect GitHub repo `tigerzhang153/bookie`
   - **Branch**: `^main$`
   - **Configuration**: Cloud Build configuration file
   - **Location**: `cloudbuild.yaml`

5. **Click "CREATE"**

6. **Then go back to Cloud Run and set up continuous deployment to use this trigger**

## Option 3: Deploy Using gcloud CLI (If you install it)

```bash
gcloud run deploy bookie \
  --source . \
  --region us-east5 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300
```

