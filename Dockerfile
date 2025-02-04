# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/local.txt

# Make port 8080 available to the world outside this container
EXPOSE 8020

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8020"]
