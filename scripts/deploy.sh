#!/bin/bash
# Deployment script for Arigold agent to Google Cloud Functions

set -e

# Configuration
PROJECT_ID="${ARIGOLD_PROJECT_ID:-your-project-id}"
REGION="${ARIGOLD_REGION:-us-central1}"
FUNCTION_NAME="${ARIGOLD_FUNCTION_NAME:-arigold-agent}"
RUNTIME="python312"
ENTRY_POINT="arigold_agent"
SOURCE_DIR="src"

echo "=========================================="
echo "Deploying Arigold Agent to Cloud Functions"
echo "=========================================="
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Function: $FUNCTION_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the project
echo "Setting project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

# Deploy the function
echo "Deploying function..."
gcloud functions deploy "$FUNCTION_NAME" \
    --gen2 \
    --runtime="$RUNTIME" \
    --region="$REGION" \
    --source="$SOURCE_DIR" \
    --entry-point="$ENTRY_POINT" \
    --trigger-http \
    --allow-unauthenticated \
    --memory=512MB \
    --timeout=60s \
    --set-env-vars="ARIGOLD_PROJECT_ID=$PROJECT_ID,ARIGOLD_LOCATION=$REGION"

echo ""
echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Function URL:"
gcloud functions describe "$FUNCTION_NAME" \
    --region="$REGION" \
    --gen2 \
    --format="value(serviceConfig.uri)"
echo ""
echo "To test the function, run:"
echo "  ./scripts/test_function.sh"
echo ""
