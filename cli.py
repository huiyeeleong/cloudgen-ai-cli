import os
from genai_client import generate_iac

def main():
    print(" Welcome to CloudGen AI CLI\n")

    # Step-by-step inputs
    cloud = input("Which cloud provider? (aws / azure / gcp / oracle): ").strip().lower()
    while cloud not in ["aws", "azure", "gcp", "oracle"]:
        cloud = input(" Invalid. Please enter: aws / azure / gcp / oracle: ").strip().lower()

    # Supported IaC tools per cloud
    supported_iac = {
        "aws": ["cloudformation", "terraform"],
        "azure": ["bicep", "terraform"],
        "gcp": ["terraform"],
        "oracle": ["terraform"]
    }

    iac_options = supported_iac[cloud]

    print("\n💬 What is your priority for the infrastructure code?")
    print("1. Cloud-native format (e.g., CloudFormation, Bicep)")
    print("2. Cross-platform portability (e.g., Terraform)")
    print("3. Easy readability")
    print("4. I’m not sure")

    goal = input("Choose 1 / 2 / 3 / 4: ").strip()

    # Decision logic
    if goal == "1":
        if "cloudformation" in iac_options:
            iac = "cloudformation"
        elif "bicep" in iac_options:
            iac = "bicep"
        else:
            iac = iac_options[0]
            print(f"ℹ️ Defaulting to {iac}")
    elif goal == "2":
        iac = "terraform"
    elif goal == "3":
        iac = iac_options[0]
        print(f"ℹ️ Choosing most readable option: {iac}")
    else:
        if len(iac_options) == 1:
            iac = iac_options[0]
            print(f"ℹ️ Using default IaC tool for {cloud.upper()}: {iac}")
        else:
            iac = input(f"Which IaC tool do you prefer? ({' / '.join(iac_options)}): ").strip().lower()
            while iac not in iac_options:
                iac = input(f" Invalid. Please enter one of: ({' / '.join(iac_options)}): ").strip().lower()

    service = input("What service to deploy? (e.g., ec2, s3, lambda, vm): ").strip().lower()
    access = input("Does it need access to other services? (yes / no): ").strip().lower()
    vpc = input("Do you have a virtual network/subnet already? (yes / no): ").strip().lower()

    # Build dynamic, cloud-aware prompt
    prompt = f"Generate a {iac} script for {cloud} to deploy {service}. "

    if access == "yes":
        if cloud == "aws":
            prompt += "Add IAM role for access using least privilege. "
        elif cloud == "azure":
            prompt += "Add a managed identity and assign appropriate RBAC roles. "
        elif cloud == "gcp":
            prompt += "Add a service account with least privilege. "
        elif cloud == "oracle":
            prompt += "Add IAM policy for service access using least privilege. "

    if vpc == "no":
        if cloud == "aws":
            prompt += "Create a new VPC with public/private subnets, IGW, and NAT gateway. "
        elif cloud == "azure":
            prompt += "Create a new virtual network with subnets and a NAT gateway. "
        elif cloud == "gcp":
            prompt += "Create a new VPC network with subnets and Cloud NAT. "
        elif cloud == "oracle":
            prompt += "Create a new virtual cloud network (VCN) with subnets and internet gateway. "

    prompt += (
        "Use production-grade best practices and security recommendations. "
        "Respond with only the code in plain text without any markdown or explanation."
    )

    print("\n Generating infrastructure as code with GenAI...\n")
    output = generate_iac(prompt)

    # Write to mounted output directory
    extension_map = {
        "cloudformation": "yaml",
        "terraform": "tf",
        "bicep": "bicep"
    }
    extension = extension_map.get(iac, "txt")
    filename = f"{cloud}-{service}.{extension}"
    output_dir = "/home/cliuser/output"
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    with open(full_path, "w") as f:
        f.write(output)

    print(f"\n✅ IaC written to: {full_path}")

if __name__ == "__main__":
    main()
