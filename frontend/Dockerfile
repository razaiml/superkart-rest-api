# Using a minimal base image with Python 3.11.9 installed
FROM python:3.11.9-slim

# Setting the working directory inside the container to /app
WORKDIR /app

# Copying all files from the current directory on the host to the container's /app directory
COPY . .

# Installing Python dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# Defining the command to run the Streamlit app on port 8501 and make it accessible externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]

# NOTE: Disable XSRF protection for easier external access in order to make batch predictions
