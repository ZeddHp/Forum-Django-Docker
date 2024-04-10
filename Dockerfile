# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /myforum

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /myforum/

# Collect static files
RUN python myforum/manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

CMD ["python3", "myforum/manage.py", "runserver", "0.0.0.0:8000"]
