```dockerfile
FROM rasa/rasa:3.6.18-full

# Switch to root user to install dependencies
USER root

# Copy the project files
COPY . /app

# Set working directory
WORKDIR /app

# Install any additional dependencies if needed
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the start script and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Switch back to the rasa user
USER 1001

# Run the start script
CMD ["/app/start.sh"]
```