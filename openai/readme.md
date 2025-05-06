## Project Overview

This project provides a toolchain for generating and validating AWS CloudFormation templates using OpenAI's language models. It consists of a Bash script (`openai-aws.sh`) and a Python script (`openai.py`). The workflow allows users to describe AWS infrastructure in natural language, generate a CloudFormation YAML template, and validate the template for deployment on AWS.

---

## Files

**openai-aws.sh**

- Bash script to automate the process of:
    - Accepting an infrastructure description as input.
    - Calling `openai.py` to generate a CloudFormation template.
    - Validating the generated template using AWS CLI.
    - Performing a dry-run deployment to ensure deployability.
- Usage:

```sh
./openai-aws.sh "Describe your AWS infrastructure"
```

- Requirements:
    - AWS CLI configured with appropriate permissions.
    - Python (for running `openai.py`).
    - `openai.py` and `values.yaml` in the same directory.

**openai.py**

- Python script to generate AWS CloudFormation YAML templates using OpenAI's GPT models.
- Accepts:
    - A prompt describing the desired AWS infrastructure.
    - (Optional) A YAML file with values to be used in the template.
- Outputs:
    - A YAML file (`template-&lt;hash&gt;.yaml`) containing the generated CloudFormation template.
- Usage:

```sh
python openai.py "Describe your AWS infrastructure" --values values.yaml
```

- Requirements:
    - Python 3.x
    - `openai` Python package
    - `pyyaml` package

---

## Quick Start

1. Ensure AWS CLI and Python dependencies are installed and configured.
2. Prepare a `values.yaml` file if you want to provide specific values.
3. Run the Bash script:

```sh
./openai-aws.sh "Your infrastructure description"
```

4. The script will generate and validate the CloudFormation template.

---

## Notes

- The OpenAI API key must be configured in your environment for `openai.py` to function.
- The generated template is validated and tested with a dry-run deployment, but not actually deployed.
- For more customization, edit `values.yaml` or modify the prompt as needed.

---

Feel free to ask if you need a sample `values.yaml`, more usage examples, or details on extending this workflow!

<div style="text-align: center">⁂</div>

[^1_1]: openai-aws.sh

[^1_2]: openai.py
