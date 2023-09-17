# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variables for  API key and database credentials
ENV API_KEY ""
ENV DB_USER ""
ENV DB_PASSWORD ""

# Run ETL script (app.py) when the container launches
CMD ["python", "app.py"]
