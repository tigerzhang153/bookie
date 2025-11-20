# Deploy API to Firebase Functions

## Deploy Steps

1. **Deploy Functions:**
   ```bash
   firebase deploy --only functions
   ```

2. **The API will be available at:**
   `https://us-central1-bookie-ai-dc1f8.cloudfunctions.net/api`

3. **Endpoints:**
   - Health: `https://us-central1-bookie-ai-dc1f8.cloudfunctions.net/api/health`
   - Predict: `https://us-central1-bookie-ai-dc1f8.cloudfunctions.net/api/predict`

4. **Update Frontend Config:**
   The config.js is already updated. Just rebuild and redeploy:
   ```bash
   npm run build
   firebase deploy --only hosting
   ```

## Notes

- Firebase Functions uses Cloud Run under the hood (2nd gen functions)
- Memory: 2GB (configured in main.py)
- Timeout: 300 seconds
- The model file (149MB) will be included in the deployment
- First deployment may take 10-15 minutes

