FROM rasa/rasa-sdk:3.6.18

# Switch to root user to install dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-actions.txt /app/requirements-actions.txt
RUN pip install --no-cache-dir -r /app/requirements-actions.txt

# Copy actions
COPY . /app/actions

# Switch back to the rasa user
USER 1001

# Set the working directory
WORKDIR /app

# Expose the port
EXPOSE 5055

# Run the action server
CMD ["start", "--actions", "actions.actions", "--debug"]