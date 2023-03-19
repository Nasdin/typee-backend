ARG BUCKET_NAME
ENV BUCKET_NAME=${BUCKET_NAME}

ARG GOOGLE_API_KEY
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

ARG GOOGLE_CSE_ID
ENV GOOGLE_CSE_ID=${GOOGLE_CSE_ID}

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Create the Firebase credentials file from the environment variable
ARG FIREBASE_ADMINSDK_JSON
ENV FIREBASE_ADMINSDK_JSON_FILE /app/firebase-adminsdk.json
RUN echo $FIREBASE_ADMINSDK_JSON > $FIREBASE_ADMINSDK_JSON_FILE

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Run gunicorn when the container launches
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]