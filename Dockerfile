# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create download folder to avoid runtime errors
RUN mkdir -p /app/downloads/telegram

# Copy the entire project files into the container
COPY . .

# Run the bot script
CMD ["python", "movie_download.py"]
