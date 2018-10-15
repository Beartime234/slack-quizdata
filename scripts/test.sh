#!/usr/bin/env bash

SECRETS_NAME="pokequiz-secrets"  # The name of the secret in secrets manager that stores
AWS_PROFILE="beartimeworks"  # Your AWS profile that you have set up
REGION="us-east-1"

# Fix for pytest wont be able to import applications
export PYTHONPATH=uploader

echo "Running Tests"
pipenv run python -m pytest tests/ -vv