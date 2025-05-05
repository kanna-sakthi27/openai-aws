### CloudFormation Template Generator with OpenAI
Generate, validate, and dry-run AWS CloudFormation templates using OpenAI's GPT-4o model, all from the command line.

## Features
1. Natural Language to CloudFormation: Describe your AWS infrastructure in plain English.

2. Automatic Template Generation: Uses OpenAI to generate valid CloudFormation YAML.

3. Custom Value Injection: Optionally inject your own values via a YAML file.

4. Validation & Dry-Run: Validates syntax and performs a dry-run deployment using AWS CLI.

## Requirements
Operating System: Linux or macOS (Windows with WSL may work)

Python: 3.8+

Bash: 4.x+

AWS CLI: v2

OpenAI Python SDK: Latest version

pyyaml: Latest version

Installation
Clone this repository:

bash
git clone <your-repo-url>
cd <your-repo-directory>
Install Python dependencies:

bash
pip install openai pyyaml
Install AWS CLI:
Follow AWS CLI installation instructions.

Configure AWS credentials:

bash
aws configure
Set your OpenAI API key:

bash
export OPENAI_API_KEY=sk-...
Usage
1. Generate & Validate a CloudFormation Template
Run the Bash script with your infrastructure description:

bash
./openai-aws.sh "A VPC with two public subnets and an internet gateway"
The script will:

Generate a CloudFormation template using OpenAI.

Validate the template with AWS CLI.

Perform a dry-run deployment (no resources are created).

Output the template file name if successful.

2. Direct Python Usage
Run the Python script directly:

bash
python openai.py "A Lambda function triggered by S3 uploads"
With custom values:

bash
python openai.py "A Lambda function triggered by S3 uploads" --values values.yaml
File Descriptions
openai.py
Python script for template generation using OpenAI.

openai-aws.sh
Bash script for automated generation, validation, and dry-run.

values.yaml (optional)
YAML file for injecting custom values into your template.

Example
values.yaml:

text
BucketName: my-unique-bucket
FunctionName: my-lambda-func
Command:


``` ./openai-aws.sh "A Lambda function triggered by S3 uploads"```