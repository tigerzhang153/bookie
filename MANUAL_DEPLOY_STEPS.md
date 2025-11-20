# Manual Deployment Steps for Cloud Run

Since continuous deployment isn't set up, here's how to deploy:

## Option 1: Create Cloud Build Trigger (Recommended)

1. **Go to Cloud Build Triggers:**
   https://console.cloud.google.com/cloud-build/triggers?project=bookie-ai-dc1f8

2. **Click "CREATE TRIGGER"**

3. **Configure:**
   - **Name**: `bookie-api-deploy`
   - **Event**: Push to a branch
   - **Source**: Connect your GitHub repository `tigerzhang153/bookie`
   - **Branch**: `^main$` (regex pattern)
   - **Configuration**: Cloud Build configuration file (yaml or json)
   - **Location**: `cloudbuild.yaml` (in root of repo)

4. **Click "CREATE"**

5. **Manually run the trigger:**
   - Click on the trigger you just created
   - Click "RUN" to trigger a build now

## Option 2: Manual Build via Cloud Build

1. **Go to Cloud Build:**
   https://console.cloud.google.com/cloud-build/builds?project=bookie-ai-dc1f8

2. **Click "RUN HISTORY"**

3. **Click "RUN A BUILD"**

4. **Configure:**
   - **Source**: GitHub
   - **Repository**: `tigerzhang153/bookie`
   - **Branch**: `main`
   - **Configuration**: Cloud Build configuration file
   - **Cloud Build configuration file location**: `cloudbuild.yaml`

5. **Click "RUN"**

This will use the `cloudbuild.yaml` file which builds from the `api/` directory.

## What the cloudbuild.yaml Does

- Builds Docker image from `api/Dockerfile`
- Uses `api` as the build context
- Pushes to Container Registry
- Deploys to Cloud Run service `bookie` in `us-east5`

The build should work now!

