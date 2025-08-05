FROM rasa/rasa:3.6.18-full

# Switch to root user to install dependencies
USER root

# Copy the project files
COPY . /app

# Set working directory
WORKDIR /app

# Install any additional dependencies if needed
# RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the rasa user
USER 1001

# Train the model
RUN rasa train

# Expose the port
EXPOSE 5005

# Run Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug"]