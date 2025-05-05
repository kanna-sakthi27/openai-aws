#!/bin/bash

REGION="ap-southeast-2" # 


# Validate input
if [ $# -eq 0 ]; then
    echo "Error: Please provide infrastructure description"
    echo "Usage: $0 \"Your infrastructure description\""
    exit 1
fi

# Generate CloudFormation template
echo "Generating CloudFormation template..."
output=$(python openai.py "$1"  --values values.yaml )
filename=$(echo "$output" | grep -oP 'template-\d+.yaml')

# Check template generation
if [ ! -f "$filename" ]; then
    echo "Template generation failed!"
    exit 2
fi

# AWS validation functions
validate_template() {
    echo "Validating template syntax..."
    aws cloudformation validate-template \
        --template-body "file://$filename" >/dev/null 2>&1
    return $?
}

dry_run_deployment() {
    local stack_name="temp-stack-$(date +%s)"
    local change_set_name="dry-run-$(date +%s)"
    
    echo "Performing dry-run deployment..."
    aws cloudformation create-change-set \
        --stack-name "$stack_name" \
        --template-body "file://$filename" \
        --change-set-name "$change_set_name" \
        --region $REGION \
        --change-set-type "CREATE" >/dev/null

        #--capabilities CAPABILITY_IAM \
    
    aws cloudformation wait change-set-create-complete \
        --stack-name "$stack_name" \
        --region $REGION \
        --change-set-name "$change_set_name" >/dev/null 2>&1

    
    local status=$?
    
    # Cleanup resources
    aws cloudformation delete-change-set \
        --stack-name "$stack_name" \
        --region $REGION \
        --change-set-name "$change_set_name" >/dev/null
    
    return $status
}

# Run validation checks
if validate_template; then
    echo "✅ Template syntax valid"
else
    echo "❌ Template syntax invalid"
    exit 3
fi

if dry_run_deployment; then
    echo "🚀 Dry-run succeeded - template can be deployed"
else
    echo "❌ Dry-run failed - check resource configuration"
    exit 4
fi

echo "Validation complete. Template ready: $filename"
