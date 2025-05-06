#!/bin/bash

# Usage: ./deploy.sh "your command" [--values values.yaml]
REGION="ap-southeast-2" # 

DESCRIPTION="$1"
VALUES_ARG="$2 $3"  # In case --values is provided

if [ -z "$DESCRIPTION" ]; then
    echo "Error: Please provide an English description or command."
    echo "Usage: $0 \"Your command\" [--values values.yaml]"
    exit 1
fi

# Convert to lowercase for matching
DESC_LOWER=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]')

if [[ "$DESC_LOWER" == *"start"* ]] || [[ "$DESC_LOWER" == *"stop"* ]]; then
    # Just call the Python script for start/stop logic (no CloudFormation)
    python3 ec2state-main.py "$DESCRIPTION" 
    exit $?
fi

# Otherwise, generate CloudFormation and validate
echo "Generating CloudFormation template..."
FILENAME=$(python3 main.py "$DESCRIPTION" --values values.yaml | tail -1)

if [ ! -f "$FILENAME" ]; then
    echo "Template generation failed!"
    exit 2
fi

echo "Validating template syntax..."
if aws cloudformation validate-template --template-body "file://$FILENAME" >/dev/null 2>&1; then
    echo "✅ Template syntax valid"
else
    echo "❌ Template syntax invalid"
    exit 3
fi

STACK_NAME="temp-stack-$(date +%s)"
CHANGE_SET_NAME="dry-run-$(date +%s)"

echo "Performing dry-run deployment..."
aws cloudformation create-change-set \
    --stack-name "$STACK_NAME" \
    --template-body "file://$FILENAME" \
    --change-set-name "$CHANGE_SET_NAME" \
    --region $REGION \
    --capabilities CAPABILITY_NAMED_IAM \
    --change-set-type "CREATE" >/dev/null

#!/bin/bash

# Wait for changeset creation process
sleep 10 

# Describe Change Set to perform dry run
aws cloudformation describe-change-set \
    --stack-name "$STACK_NAME" \
    --region $REGION \
    --capabilities CAPABILITY_NAMED_IAM \
    --change-set-name "$CHANGE_SET_NAME" >/dev/null 2>&1

DRY_RUN_STATUS=$?

if [ $DRY_RUN_STATUS -eq 0 ]; then
    echo ":rocket: Dry-run succeeded - template can be deployed"
else
    echo ":x: Dry-run failed - check resource configuration"
    exit 4
fi

# Cleanup after successful validation only
echo "Performing cleanup deployment..."

aws cloudformation delete-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$CHANGE_SET_NAME" \
  --region $REGION \

echo "Validation complete."