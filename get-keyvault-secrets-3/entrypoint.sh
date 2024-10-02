#!/usr/bin/env bash 

# Set environment variables
KEYVAULT=$1
SECRETS=$2

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
