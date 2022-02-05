#!/bin/sh
set -eux

OPENAPI_RUN_FILE=../espv2/openapi-run.yaml

python manage.py spectacular --file openapi-schema.yaml

api-spec-converter --from=openapi_3 --to=swagger_2 --syntax=yaml openapi-schema.yaml > "${OPENAPI_RUN_FILE}"

# remove last slash in each endpoint definition
gsed -i 's/\/:/:/g' "${OPENAPI_RUN_FILE}"

# replace `in: cookie` with `in: header` as the value "cookie" is invalid
gsed -i 's/in: cookie/in: header/' "${OPENAPI_RUN_FILE}"

ESP_V2_PARTS="host: espv2-simple-auth-app-dev-4r4bp3qvaq-an.a.run.app\nschemes:\n  - https\nproduces:\n  - application/json\nx-google-backend:\n  address: https://simple-auth-app-4r4bp3qvaq-an.a.run.app\n  protocol: h2"

gsed -e "/paths:/i ${ESP_V2_PARTS}" -i "${OPENAPI_RUN_FILE}"
