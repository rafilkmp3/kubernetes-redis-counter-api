FROM python:3.9-slim

# Create a non-root user and group with a specific UID and GID
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/false appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src .

# Change ownership of the working directory to the non-root user
RUN chown -R 1001:1001 /app

# Switch to the non-root user using numeric UID
USER 1001

# Expose the port and define the command to run the application
EXPOSE 5000

# Start Gunicorn (no need to specify --worker-tmp-dir since /tmp is writable)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
