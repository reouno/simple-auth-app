#!/bin/sh
set -eux

# Build
gcloud builds submit --config cloudmigrate.yaml

# Deploy
gcloud run deploy simple-auth-app \
    --platform managed \
    --region asia-northeast1 \
    --image gcr.io/simple-auth-app-dev/simple-auth-app