# Use an official Python image
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium-driver \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the local files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add Chrome and ChromeDriver paths
ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_DRIVER_PATH="/usr/bin/chromedriver"

# Run the Python script every hour
CMD ["sh", "-c", "while true; do python script.py; sleep 3600; done"]
