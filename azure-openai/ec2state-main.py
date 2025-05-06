import os
import sys
import boto3
import json
from openai import AzureOpenAI

# Set your Azure OpenAI deployment details
AZURE_OPENAI_ENDPOINT = "https://api-dev.workspace.xxxxx.com/dev/aoai/api/"  # e.g. "https://<your-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")           # Your Azure OpenAI API key
AZURE_OPENAI_DEPLOYMENT = "gpt-4o"  # e.g. "gpt-4o-2024-05-13"

def get_intent_and_instance(user_input, client, deployment):
    prompt = (
        "You are an assistant that extracts the intended AWS EC2 action and instance name from the user's request. "
        "Reply in JSON with two keys: 'action' (start, stop, or restart) and 'instance_name' (the EC2 Name tag value). "
        "If either is missing, set its value to null.\n\n"
        f"User request: {user_input}"
    )
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content
    try:
        # Find and parse JSON object in the response
        start = content.find('{')
        end = content.rfind('}') + 1
        json_str = content[start:end]
        data = json.loads(json_str)
        return data.get("action"), data.get("instance_name")
    except Exception as e:
        print(f"Could not parse OpenAI response: {e}\nRaw response: {content}")
        return None, None

def get_instance_ids_by_name(name):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Name', 'Values': [name]}]
    )
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    return instance_ids

def start_instances(instance_ids):
    ec2 = boto3.client('ec2')
    ec2.start_instances(InstanceIds=instance_ids)
    print(f"Started instances: {instance_ids}")

def stop_instances(instance_ids):
    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=instance_ids)
    print(f"Stopped instances: {instance_ids}")

def restart_instances(instance_ids):
    ec2 = boto3.client('ec2')
    ec2.reboot_instances(InstanceIds=instance_ids)
    print(f"Restarted instances: {instance_ids}")

def main():
    if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY and AZURE_OPENAI_DEPLOYMENT):
        print("Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_DEPLOYMENT environment variables.")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("Usage: python script.py \"<your request in English>\"")
        sys.exit(1)
    user_input = " ".join(sys.argv[1:])

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version="2024-02-01"
    )

    action, instance_name = get_intent_and_instance(user_input, client, AZURE_OPENAI_DEPLOYMENT)
    if not action or not instance_name:
        print("Could not determine action or instance name from your input.")
        sys.exit(1)

    instance_ids = get_instance_ids_by_name(instance_name)
    if not instance_ids:
        print(f"No EC2 instances found with Name tag '{instance_name}'")
        sys.exit(1)

    if action == "start":
        start_instances(instance_ids)
    elif action == "stop":
        stop_instances(instance_ids)
    elif action == "restart":
        restart_instances(instance_ids)
    else:
        print(f"Unsupported action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
