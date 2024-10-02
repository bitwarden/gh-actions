#!/usr/bin/env bash 

# Set environment variables
CREDS=$1
KEYVAULT=$2
SECRETS=$3

APP_ID=$(echo ${CREDS} | jq -r .appId)
PASSWORD=$(echo ${CREDS} | jq -r .password)
TENANT=$(echo ${CREDS} | jq -r .tenant)

az login --service-principal -u $APP_ID -p $PASSWORD --tenant $TENANT
echo $?

# Create empty JSON file
echo "{}" > output.json

# Remove spaces from secrets list
SECRET_LIST=$(echo "$SECRETS" | tr -d '[:space:]')

# Loop over secret names and add them to the JSON file
for i in ${SECRET_LIST//,/ }
do
    SECRET=$(az keyvault secret show --vault-name $KEYVAULT --name $i --query 'value')
    echo "::add-mask::$SECRET"
    echo "$i=$SECRET" >> $GITHUB_OUTPUT
done
