## AWS + Azure OpenAI CloudFormation Automation Toolkit

This toolkit enables you to generate, validate, and dry-run AWS CloudFormation templates from natural language descriptions using Azure OpenAI or OpenAI APIs. It also supports direct EC2 instance state management (start/stop/restart) via natural language commands.

---

## Contents

- **gen-aws.sh**
Bash script to orchestrate the workflow:
    - Accepts a natural language command or infrastructure description.
    - Detects EC2 start/stop/restart requests and delegates to `ec2state-main.py`.
    - For other requests, generates a CloudFormation template using `main.py`, validates it, and performs a dry-run deployment using AWS CLI.
    - Cleans up temporary AWS resources after validation.
- **main.py**
Python script to generate AWS CloudFormation YAML templates from a prompt using Azure OpenAI.
    - Reads a prompt and optional values from a YAML file.
    - Connects to Azure OpenAI (or compatible endpoint) using provided credentials.
    - Outputs a CloudFormation YAML file named `template-&lt;hash&gt;.yaml`.
- **ec2state-main.py**
Python script for direct EC2 instance management:
    - Uses Azure OpenAI to extract the intended EC2 action (start, stop, restart) and instance name from a natural language command.
    - Uses boto3 to perform the action on AWS EC2 instances matching the given Name tag.
- **values.yaml**
Optional YAML file to supply parameter values for template generation.

---

## Quick Start

1. **Set up environment variables:**
    - For Azure OpenAI:
        - `AZURE_OPENAI_ENDPOINT`
        - `AZURE_OPENAI_KEY`
        - `AZURE_OPENAI_DEPLOYMENT`
    - For AWS:
        - Configure AWS CLI with appropriate permissions.
2. **Install dependencies:**
    - Python 3.x, `boto3`, `pyyaml`, `openai` (or compatible), `azure-openai` Python packages.
3. **Usage:**
    - Generate/validate a CloudFormation template:

```sh
./gen-aws.sh "Create an S3 bucket with versioning enabled" [--values values.yaml]
```

    - Start/stop/restart an EC2 instance by name:

```sh
./gen-aws.sh "Start the web-server instance"
./gen-aws.sh "Stop the analytics-server"
./gen-aws.sh "Restart the dev-server"
```


---

## How It Works

| Script | Purpose | Input Example |
| :-- | :-- | :-- |
| gen-aws.sh | Main entrypoint, routes commands, validates templates | `"Create a VPC with 2 subnets"` |
| main.py | Generates CloudFormation YAML via Azure OpenAI | Prompt and optional `values.yaml` |
| ec2state-main.py | Parses and executes EC2 start/stop/restart commands | `"Stop the database-server"` |
| values.yaml | Supplies parameter values for template generation | See your own `values.yaml` structure |


---

## Notes

- Ensure your OpenAI/Azure OpenAI API keys and endpoints are set as environment variables for security.
- The toolkit does not deploy resources by default; it only validates and dry-runs CloudFormation templates.
- For EC2 state changes, ensure your AWS credentials allow the necessary EC2 actions.

---