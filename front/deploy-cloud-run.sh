#!/bin/sh
set -eux

PROJECT_ID=simple-auth-app-dev
SERVICE_NAME=front-simple-auth-app-dev
REGION=asia-northeast1
IMAGE=gcr.io/${PROJECT_ID}/${SERVICE_NAME}
NUXT_ENV_BASE_URL=https://espv2-simple-auth-app-dev-4r4bp3qvaq-an.a.run.app

gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _PROJECT_ID=${PROJECT_ID},_SERVICE_NAME=${SERVICE_NAME},_NUXT_ENV_BASE_URL=${NUXT_ENV_BASE_URL} \

gcloud run deploy ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --image ${IMAGE} \
    --allow-unauthenticated


