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
BUILD_STACK_NAME="${STAGE}-${SERVICE}-build"  # The name of the stack. You could just but ${SERVICE} here

# File Pathing
TEMPLATE_FOLDER="templates"  # The folder which your template lives in
BUILD_TEMPLATE_FILE="build.yml"  # the file that in your template folder it lives in
REPOSITORY_LINK="https://github.com/Beartime234/slack-quizdata.git"
UPLOAD_BRANCH_FILTER="(master)"
TEST_BRANCH_FILTER="(releases\/.*)"

# Export our set Aws Profile
export AWS_PROFILE=${AWS_PROFILE}

echo "CloudFormation deploying..."

aws cloudformation deploy  \
    --region ${REGION} \
    --template-file ${TEMPLATE_FOLDER}/${BUILD_TEMPLATE_FILE} \
    --stack-name ${BUILD_STACK_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-override Stage=${STAGE} ServiceName=${SERVICE} CodeCommitRepoUrl=${REPOSITORY_LINK} || true


if [[ ${STAGE} = "prod" ]]; then
   echo "Adding Webhooks"

   aws codebuild create-webhook \
    --project-name ${STAGE}-${SERVICE}-upload \
    --branch-filter ${UPLOAD_BRANCH_FILTER} \
    --region ${REGION}

   aws codebuild create-webhook \
    --project-name ${STAGE}-${SERVICE}-test \
    --branch-filter ${TEST_BRANCH_FILTER} \
    --region ${REGION}
fi

echo "CloudFormation outputs..."
aws cloudformation describe-stacks \
    --stack-name ${BUILD_STACK_NAME} \
    --query 'Stacks[].Outputs' \
    --region ${REGION}