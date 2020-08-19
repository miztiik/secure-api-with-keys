#!/bin/bash
set -ex
set -o pipefail

# version: 18Aug2020

##################################################
#############     SET GLOBALS     ################
##################################################

# cd "./api_testing_scripts"
LOG_FILE_NAME="miztiik_secure_api_with_keys.log"
SECURE_API_WITH_KEYS_URL="https://yy8eanv9j4.execute-api.us-east-1.amazonaws.com/miztiik/secure/greeter"
DEV_KON_API_KEY="F9ZufzJTa73OU1V1TEKRn10mfip1q2tG2xjblFCS"
# curl -s --header "X-API-Key: ${DEV_KON_API_KEY}" -X GET "${SECURE_API_WITH_KEYS_URL}" >> "${LOG_FILE_NAME}" &
> "${LOG_FILE_NAME}" 
for i in {1..30}
do
   curl -s -w '{"status": "%{http_code}"}\n' --header "X-API-Key: ${DEV_KON_API_KEY}" -X GET "${SECURE_API_WITH_KEYS_URL}" >> "${LOG_FILE_NAME}" &
done
