# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set PYTHONPATH to include the directory where 'app' module is located
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
# Only copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to support live reloading
ENV PYTHONUNBUFFERED 1

# Command to run when starting the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
