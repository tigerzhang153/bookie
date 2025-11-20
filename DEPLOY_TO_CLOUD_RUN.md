# Deploy to Google Cloud Run (Free Tier)

## Step 1: Deploy via Google Cloud Console

1. **Go to Cloud Run Console:**
   https://console.cloud.google.com/run?project=bookie-ai-dc1f8

2. **Click "CREATE SERVICE"**

3. **Configure the service:**
   - **Deploy one revision from a source repository**: Select this option
   - **Select a source**: Click "CONNECT REPOSITORY"
     - Choose "GitHub (Cloud Build)"
     - Authenticate and select your repo: `tigerzhang153/bookie`
   - **Source**: Select `api` directory
   - **Build type**: Dockerfile (it will automatically detect `api/Dockerfile`)
   - **Service name**: `bookie-api`
   - **Region**: `us-central1` (or closest to you)
   - **Authentication**: ✅ **Allow unauthenticated invocations** (IMPORTANT!)
   - **Container port**: `8080`
   - **Memory**: `2 GiB`
   - **CPU**: `2`
   - **Timeout**: `300 seconds`
   - **Max instances**: `10`

4. **Click "CREATE"** and wait 5-10 minutes for deployment

5. **Copy the Service URL** (will look like: `https://bookie-api-xxxxx-uc.a.run.app`)

## Step 2: Update Config

After you get the URL, share it with me and I'll update `src/config.js`, or update it yourself:

```javascript
const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://bookie-api-xxxxx-uc.a.run.app'  // Your Cloud Run URL
    : 'http://localhost:8000'
}
```

## Step 3: Rebuild and Redeploy Frontend

```bash
npm run build
firebase deploy --only hosting
```

## Free Tier Information

✅ **Cloud Run Free Tier:**
- 2 million requests per month FREE
- 400,000 GB-seconds of compute time FREE
- 200,000 GiB-seconds of memory time FREE
- You only pay if you exceed these limits

For a typical API, you'll likely stay within the free tier!

## Test After Deployment

1. Health check: `https://your-url-uc.a.run.app/health`
2. Should return: `{"status":"healthy"}`

