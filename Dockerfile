# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /companyapi

# Install dependencies
COPY requirements.txt /companyapi/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /companyapi
COPY . /companyapi/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
