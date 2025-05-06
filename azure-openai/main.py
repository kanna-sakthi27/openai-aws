import sys
import argparse
import yaml
from openai import AzureOpenAI  # Make sure you have openai >= 1.0.0 installed

def generate_cloudformation_template(prompt, values_dict, client, model_deployment_id):
    system_msg = "Generate valid AWS CloudFormation YAML templates. Respond ONLY with YAML code, no markdown formatting."
    if values_dict:
        values_str = "\n".join([f"{k}: {v}" for k, v in values_dict.items()])
        system_msg += f"\n\nUse the following values in the template where appropriate:\n{values_str}"

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model_deployment_id,
        messages=messages
    )

    generated_yaml = response.choices[0].message.content.strip()

    if generated_yaml.startswith("```yaml"):
        generated_yaml = generated_yaml[7:-3].strip()
    if generated_yaml.startswith("```yaml"):
        generated_yaml = generated_yaml[3:-3].strip()
    return generated_yaml

def main():
    parser = argparse.ArgumentParser(description="Generate AWS CloudFormation template from natural language prompt.")
    parser.add_argument("prompt", help="Describe your AWS infrastructure")
    parser.add_argument("--values", help="Path to a YAML file with values", default=None)
    args = parser.parse_args()

    # Office OpenAI deployment details - **fill in your actual API key here**
    model_deployment_id = "gpt-4o"
    ai_platform_url = "https://api-dev.workspace.xxx.com/dev/aoai/api/"
    ai_platform_api_key = "xxxxxx"  # <-- Insert your AI Platform API key here or set via environment variable

    if not ai_platform_api_key:
        # Try to read from environment variable for better security
        ai_platform_api_key = os.getenv("AI_PLATFORM_API_KEY")
        if not ai_platform_api_key:
            print("Error: AI Platform API key not set. Set it in the script or as environment variable AI_PLATFORM_API_KEY.")
            sys.exit(1)

    # Initialize AzureOpenAI client
    client = AzureOpenAI(
        api_key=ai_platform_api_key,
        azure_endpoint=ai_platform_url,
        api_version="2024-02-01"  # Adjust if your deployment requires a different version
    )

    values_dict = None
    if args.values:
        try:
            with open(args.values, 'r') as f:
                values_dict = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading values file: {e}")
            sys.exit(1)

    try:
        template = generate_cloudformation_template(args.prompt, values_dict, client, model_deployment_id)
    except Exception as e:
        print(f"Error generating template: {e}")
        sys.exit(1)

    if template:
        filename = f"template-{abs(hash(args.prompt))}.yaml"
        try:
            with open(filename, 'w') as f:
                f.write(template)
            print(filename)  # Print filename only for bash script parsing
        except Exception as e:
            print(f"Error writing template file: {e}")
            sys.exit(1)
    else:
        print("Template generation failed!")
        sys.exit(1)

if __name__ == "__main__":
    import os
    main()
