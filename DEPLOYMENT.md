# Deployment Guide

This guide describes how to deploy the `starter-fastapi` application to Google Cloud Run.

## Prerequisites

1.  **Google Cloud Project**: Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Billing Enabled**: Ensure billing is enabled for your project.
3.  **Google Cloud SDK**: Install the `gcloud` CLI.
    ```bash
    brew install --cask google-cloud-sdk
    ```

## One-Time Setup

Run these steps once to configure your Google Cloud environment.

### 1. Setup Variables

Run these lines first so you don't have to type your project ID over and over.

**Replace the values below with your actual details:**

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export SA_NAME="github-actions-deployer"
export SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
```

Initialize gcloud with your project:

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

### 2. Enable Required APIs

Switches on the "Main Power" for the services you are using.

```bash
gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  --project=$PROJECT_ID
```

### 3. Create Infrastructure

Creates the "closet" for your images and the "bucket" for your build logs.

```bash
# Create the Docker Repository (The "Closet")
gcloud artifacts repositories create cloud-run-source-deploy \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for Cloud Run" \
    --project=$PROJECT_ID

# Create the Log Bucket (The "TV Screen" for build logs)
gcloud storage buckets create gs://$PROJECT_ID-build-logs \
    --location=$REGION \
    --project=$PROJECT_ID
```

## Manual Deployment

Once the infrastructure is set up, you can deploy directly from your local machine.

```bash
gcloud run deploy starter-fastapi \
    --source . \
    --region $REGION \
    --allow-unauthenticated
```

**Note**: The `--allow-unauthenticated` flag makes your service publicly accessible. Remove it if you want to restrict access.

## CI/CD Deployment (GitHub Actions)

The project includes a GitHub Actions workflow (`.github/workflows/google-cloudrun-docker.yml`) that automates deployment.

### 1. Configure Service Account

> [!NOTE]
> **Security Note**: This workflow uses a long-lived Service Account Key (`GCP_SA_KEY`) for simplicity. A more secure approach for production environments is **Workload Identity Federation**, which avoids managing long-lived keys. This may be added in a future update.

Create the service account and grant permissions (The "Keys").

```bash
# Create Service Account
gcloud iam service-accounts create $SA_NAME \
    --display-name="GitHub Actions Deployer" \
    --project=$PROJECT_ID

# 1. Allow running builds
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/cloudbuild.builds.editor"

# 2. Allow writing images to the registry
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/artifactregistry.writer"

# 3. Allow deploying to Cloud Run
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/run.admin"

# 4. Allow "Acting As" the service runtime (Critical for security)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"

# 5. Allow uploading code to the build bucket
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.admin"

# 6. Allow usage of service APIs
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/serviceusage.serviceUsageConsumer"
```

### 2. Generate Key

Generate a JSON key for the service account:

```bash
gcloud iam service-accounts keys create key.json \
    --iam-account=$SA_EMAIL
```

### 3. Configure GitHub Secrets

1.  Go to your GitHub repository settings -> **Secrets and variables** -> **Actions**.
2.  Add the following secrets:
    *   `GCP_PROJECT_ID`: Your Google Cloud Project ID.
    *   `GCP_SA_KEY`: The content of the `key.json` file you just generated.

### 4. Trigger Deployment

The workflow is configured to run on `workflow_dispatch` (manual trigger). Go to the **Actions** tab in your repository, select **Deploy to Cloud Run**, and click **Run workflow**.

## Configuration

Cloud Run injects the `PORT` environment variable automatically (defaulting to 8080). The application is configured to listen on this port in the `Dockerfile`.

Environment variables defined in `src/starter_fastapi/core/config.py` can be overridden in Cloud Run:

```bash
gcloud run services update starter-fastapi \
    --update-env-vars ENVIRONMENT=production,LOG_LEVEL=info
```
