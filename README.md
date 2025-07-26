# CloudGen AI CLI 

A secure, containerized GenAI CLI that generates best-practice Terraform or CloudFormation scripts using LLaMA 4 Scout via Groq API.

## Security
- Runs in Docker with no shell access
- No bash, curl, or terminal tools
- Non-root user inside container

## How to Run

```bash
docker run --rm -it your-dockerhub-username/cloudgen-ai-cli
