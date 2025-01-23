# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR .

# Copy the requirements.txt file (if you have one)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code into the container
COPY . .

# Set the PYTHONPATH environment variable to include the src directory
ENV PYTHONPATH=/src

# Run the bot
CMD ["python", "main.py"]
