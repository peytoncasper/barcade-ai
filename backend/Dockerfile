# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY . .

# Set the Flask app environment variable
ENV FLASK_APP=main.py

# Expose the port that the Flask app listens on
EXPOSE 5000

# Run the Flask app when the container launches
CMD ["python", "main.py"]