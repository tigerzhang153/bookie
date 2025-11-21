# Debug "Failed to Fetch" Error

## Common Causes

1. **CORS Issue** - Browser blocking the request
2. **Network Error** - API not reachable
3. **SSL/Certificate Issue** - HTTPS problem
4. **API Timeout** - Request taking too long

## Steps to Debug

1. **Open Browser Console** (F12 or Right-click → Inspect → Console)
   - Look for the actual error message
   - Check the Network tab to see the request

2. **Check Network Tab:**
   - Go to Network tab in browser dev tools
   - Try making a prediction
   - Look for the `/predict` request
   - Check:
     - Status code
     - Response headers
     - Request headers
     - Error message

3. **Check CORS:**
   - In Network tab, look for OPTIONS request (preflight)
   - Check if it succeeds (200) or fails
   - If it fails, CORS is the issue

4. **Verify API URL:**
   - Check `src/config.js` - should be: `https://bookie-1075298251385.us-east5.run.app`
   - Make sure it matches your Cloud Run URL

5. **Test API Directly:**
   - Open: `https://bookie-1075298251385.us-east5.run.app/health`
   - Should return: `{"status":"healthy"}`

## Quick Fixes

1. **Rebuild and redeploy frontend:**
   ```bash
   npm run build
   firebase deploy --only hosting
   ```

2. **Check if API is deployed:**
   - Go to Cloud Run console
   - Verify service is "Serving" (not "Failed")

3. **Check browser console for actual error**

