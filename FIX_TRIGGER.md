# Fix Cloud Build Trigger

## Option 1: Don't Specify Service Account (Simplest)

When creating/editing the trigger:

1. **Leave "Service account" field EMPTY or select "Default"**
2. Cloud Build will use the default service account automatically
3. This avoids the logs bucket issue

## Option 2: Create the Trigger Without Service Account

1. **Go to Cloud Build Triggers:**
   https://console.cloud.google.com/cloud-build/triggers?project=bookie-ai-dc1f8

2. **If you already created one, DELETE it and create a new one**

3. **When creating the trigger:**
   - **Name**: `bookie-api-deploy`
   - **Event**: Push to a branch
   - **Source**: GitHub repo `tigerzhang153/bookie`
   - **Branch**: `^main$`
   - **Configuration**: Cloud Build configuration file (yaml or json)
   - **Location**: `cloudbuild.yaml`
   - **Service account**: LEAVE EMPTY or select "Default (Cloud Build service account)"
   - **DO NOT** select a specific service account

4. **Click "CREATE"**

## Option 3: Manual Build (No Trigger Needed)

If triggers keep failing, you can manually build:

1. **Go to Cloud Build:**
   https://console.cloud.google.com/cloud-build/builds?project=bookie-ai-dc1f8

2. **Click "RUN A BUILD"**

3. **Select:**
   - **Source**: GitHub
   - **Repository**: `tigerzhang153/bookie`
   - **Branch**: `main`
   - **Configuration**: Cloud Build configuration file
   - **File location**: `cloudbuild.yaml`

4. **Click "RUN"**

This will build and deploy without needing a trigger.

