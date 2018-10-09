#!/usr/bin/env bash
set -e

if [ -z "$1" ]
  then
    echo "Argument stage is required"
    exit 1
fi

# Aws Variables
STAGE=$1
ACCOUNT_ID="934679804324"  # Your AWS account id
REGION="us-east-1"  # The AWS region you are building in e.g. ap-southeast-2
AWS_PROFILE="beartimeworks"  # Your AWS profile that you have set up

# Stack Variables
SERVICE="quizdata"  # The name of the service e.g. MySuperCoolSlackApp
DATA_STACK_NAME="${STAGE}-${SERVICE}"  # The name of the stack. You could just but ${SERVICE} here

# File Pathing
TEMPLATE_FOLDER="templates"  # The folder which your template lives in
DATA_TEMPLATE_FILE="data.yml"  # the file that in your template folder it lives in

# Export our set Aws Profile
export AWS_PROFILE=${AWS_PROFILE}

echo "CloudFormation deploying..."

aws cloudformation deploy  \
    --region ${REGION} \
    --template-file ${TEMPLATE_FOLDER}/${DATA_TEMPLATE_FILE} \
    --stack-name ${DATA_STACK_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-override Stage=${STAGE} ServiceName=${SERVICE} || true

echo "CloudFormation outputs..."
aws cloudformation describe-stacks \
    --stack-name ${DATA_STACK_NAME} \
    --query 'Stacks[].Outputs' \
    --region ${REGION}