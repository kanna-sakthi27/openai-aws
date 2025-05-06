import sys
import argparse
import yaml
from openai.openai import OpenAI

def generate_cloudformation_template(prompt, values_dict=None):
    client = OpenAI()
    system_msg = "Generate valid AWS CloudFormation YAML templates. Respond ONLY with YAML code, no markdown formatting."
    if values_dict:
        # Format the values for the prompt
        values_str = "\n".join([f"{k}: {v}" for k, v in values_dict.items()])
        system_msg += f"\n\nUse the following values in the template where appropriate:\n{values_str}"
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    generated_yaml = response.choices[0].message.content.strip()
    if generated_yaml.startswith("```yaml"):
        generated_yaml = generated_yaml[7:-3].strip()
    if generated_yaml.startswith("```yaml"):
        generated_yaml = generated_yaml[3:-3].strip()
    return generated_yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="Describe your AWS infrastructure")
    parser.add_argument("--values", help="Path to a YAML file with values", default=None)
    args = parser.parse_args()

    values_dict = None
    if args.values:
        with open(args.values, 'r') as f:
            values_dict = yaml.safe_load(f)

    template = generate_cloudformation_template(args.prompt, values_dict)
    if template:
        filename = f"template-{abs(hash(args.prompt))}.yaml"
        with open(filename, 'w') as f:
            f.write(template)
        print(f"{filename}")
    else:
        print("Template generation failed!")
        sys.exit(2)
