FROM python:3.11-slim

# Set non-root user
RUN useradd -ms /bin/bash cliuser
USER cliuser

# Set workdir
WORKDIR /home/cliuser/app

# Copy source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "cli.py"]
