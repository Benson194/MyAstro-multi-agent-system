#!/bin/bash
# Deployment script for Google Cloud Run
# KEY CONCEPT: Agent deployment automation

set -e

echo "🚀 Deploying MyYear.AI to Google Cloud Run"
echo "=========================================="

# Check for required environment variables
if [ -z "$GCP_PROJECT_ID" ]; then
    echo "❌ Error: GCP_PROJECT_ID not set"
    echo "Please set: export GCP_PROJECT_ID=your-project-id"
    exit 1
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY not set"
    echo "The deployment will work but you'll need to set it in Cloud Run environment"
fi

# Set variables
PROJECT_ID=$GCP_PROJECT_ID
REGION=${GCP_REGION:-us-central1}
SERVICE_NAME="myyear-ai"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "📦 Project: $PROJECT_ID"
echo "🌎 Region: $REGION"
echo "🏷️  Service: $SERVICE_NAME"
echo ""

# Build the container image
echo "🔨 Building container image..."
gcloud builds submit --tag $IMAGE_NAME --project $PROJECT_ID

echo ""
echo "✅ Image built successfully!"
echo ""

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_API_KEY=$GOOGLE_API_KEY" \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your service is available at:"
gcloud run services describe $SERVICE_NAME --region $REGION --project $PROJECT_ID --format='value(status.url)'
echo ""
echo "📚 API Documentation:"
echo "  Health: GET /health"
echo "  Upload: POST /upload"
echo "  Wrapped: POST /wrapped"
echo "  Chat: POST /chat"
echo ""
echo "🎉 Deployment successful!"


