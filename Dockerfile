FROM python:3.11-slim

# Set non-root user
RUN useradd -m cliuser
USER cliuser

WORKDIR /home/cliuser/app

# Copy files
COPY --chown=cliuser . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# No bash or shell needed; no exec-in
ENTRYPOINT ["python3", "cli.py"]
