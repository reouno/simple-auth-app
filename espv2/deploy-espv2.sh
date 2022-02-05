#!/bin/sh
set -eux

GCP_PROJECT=simple-auth-app-dev
ENDPOINTS_IMAGE=endpoints-runtime-serverless
ENDPOINTS_HOST=espv2-simple-auth-app-dev-4r4bp3qvaq-an.a.run.app

# deploy ESPv2 configuration
gcloud endpoints services deploy openapi-run.yaml \
  --project simple-auth-app-dev

# get config ID
CONFIG_ID="$(gcloud endpoints configs list \
  --service=${ENDPOINTS_HOST} \
  --sort-by='~CONFIG_ID' \
  --limit=1 \
  | tail -1 | cut -d' ' -f1)"

# build ESPv2 image
./gcloud_build_image -s "${ENDPOINTS_HOST}" \
    -c "${CONFIG_ID}" -p simple-auth-app-dev

# get image tag
ENDPOINTS_IMAGE_TAG="$(gcloud container images list-tags gcr.io/${GCP_PROJECT}/${ENDPOINTS_IMAGE} \
  --sort-by=timestamp | tail -1 | cut -d' ' -f3)"

# deploy image to Cloud Run
gcloud run deploy espv2-simple-auth-app-dev \
  --image="gcr.io/simple-auth-app-dev/endpoints-runtime-serverless:${ENDPOINTS_IMAGE_TAG}" \
  --allow-unauthenticated \
  --platform managed \
  --project ${GCP_PROJECT}
