
# CloudFormation Automation Toolkit (OpenAI \& Azure OpenAI)

This toolkit enables you to **generate, validate, and dry-run AWS CloudFormation templates** from natural language descriptions using either OpenAI or Azure OpenAI APIs. It also supports direct EC2 instance management (start/stop/restart) via natural language commands.

---

## Features

- **Natural Language to CloudFormation:**
Describe your desired AWS infrastructure in plain English and generate a ready-to-deploy CloudFormation YAML template.
- **Template Validation and Dry-Run:**
Automatically validate the generated template and perform a dry-run deployment using AWS CLI.
- **EC2 Instance State Management:**
Start, stop, or restart EC2 instances by name using natural language commands.
- **Supports Both OpenAI and Azure OpenAI:**
Choose your preferred LLM backend.

---

## File Overview

| File | Purpose |
| :-- | :-- |
| `openai-aws.sh` | Bash script for OpenAI-based template generation \& validation |
| `openai.py` | Python script for OpenAI-based CloudFormation generation |
| `gen-aws.sh` | Bash script for Azure OpenAI-based workflow \& EC2 management |
| `main.py` | Python script for Azure OpenAI-based CloudFormation generation |
| `ec2state-main.py` | Python script for EC2 state management via Azure OpenAI + AWS |
| `values.yaml` | (Optional) YAML file for parameter values used in template generation |


---

## Quick Start

### 1. Prerequisites

- **AWS CLI** configured with credentials and permissions
- **Python 3.x** with packages: `openai`, `boto3`, `pyyaml`
- For Azure OpenAI: `azure-openai` or compatible library


### 2. Environment Variables

#### For OpenAI:

- `OPENAI_API_KEY` (if using `openai.py`)


#### For Azure OpenAI:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_DEPLOYMENT`

---

### 3. Usage

#### A. Generate and Validate CloudFormation Template

**Using OpenAI:**

```sh
./openai-aws.sh "Create an S3 bucket with versioning enabled"
```

**Using Azure OpenAI:**

```sh
./gen-aws.sh "Create a VPC with 2 subnets" [--values values.yaml]
```


#### B. EC2 Instance State Management (Azure OpenAI only)

```sh
./gen-aws.sh "Start the web-server instance"
./gen-aws.sh "Stop the analytics-server"
./gen-aws.sh "Restart the dev-server"
```


---

## How It Works

1. **Template Generation:**
    - The bash script (`openai-aws.sh` or `gen-aws.sh`) passes your prompt to the relevant Python script (`openai.py` or `main.py`), which uses the LLM to generate CloudFormation YAML.
2. **Validation \& Dry-Run:**
    - The script validates the YAML with AWS CLI and performs a dry-run deployment using CloudFormation change sets.
3. **EC2 Management:**
    - For EC2 commands, `gen-aws.sh` routes the request to `ec2state-main.py`, which uses Azure OpenAI to extract intent and instance name, then uses boto3 to manage the instance.

---

## Example `values.yaml`

```yaml
BucketName: my-unique-bucket
Environment: production
InstanceType: t3.micro
```


---

## Notes

- **No real resources are deployed** by default; only validation and dry-run are performed.
- For EC2 state changes, ensure your AWS credentials allow the necessary actions.
- For best results, provide clear and specific infrastructure descriptions.
- You may use either OpenAI or Azure OpenAI workflows as suits your environment.

---

## Troubleshooting

- **API Keys/Endpoints:** Ensure all required environment variables are set.
- **Dependencies:** Install all required Python packages.
- **Template Generation Fails:** Check your prompt clarity and LLM API access.

---

## Extending

- Integrate additional resource types by enhancing prompt templates.
- Support other cloud providers by adapting the Python scripts.

---