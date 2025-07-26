import sys
from genai_client import generate_iac

def main():
    print("🌩️ Welcome to CloudGen AI CLI")

    cloud = input("Which cloud provider? (aws/azure/gcp/oracle): ").strip().lower()
    iac = input("Which IaC tool? (cloudformation/terraform): ").strip().lower()
    service = input("What service to deploy? (e.g., ec2, s3, lambda, vm): ").strip().lower()
    access = input("Does it need access to other services? (yes/no): ").strip().lower()
    vpc = input("Do you have a virtual network/subnet already? (yes/no): ").strip().lower()

    # Friendly cloud-specific language
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
        else:
            prompt += "Add access permissions using the cloud provider's best practices. "

    if vpc == "no":
        if cloud == "aws":
            prompt += "Create a new VPC with public/private subnets, IGW, and NAT gateway. "
        elif cloud == "azure":
            prompt += "Create a new virtual network with subnets and a NAT gateway. "
        elif cloud == "gcp":
            prompt += "Create a new VPC network with subnets and Cloud NAT. "
        elif cloud == "oracle":
            prompt += "Create a new virtual cloud network (VCN) with subnets and internet gateway. "
        else:
            prompt += "Set up networking following the cloud provider's best practices. "

    prompt += "Use production-grade best practices and security recommendations."

    print("\n🧠 Generating infrastructure as code with GenAI...\n")
    output = generate_iac(prompt)

    filename = f"output.{ 'yaml' if iac == 'cloudformation' else 'tf' }"
    with open(filename, "w") as f:
        f.write(output)

    print(f"\nIaC written to: {filename}")

if __name__ == "__main__":
    main()
