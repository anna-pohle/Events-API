# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for Flask
# eigtl nur sinnvoll, wenn 2 verschiedene docker-container miteinander kommunizieren müssen.
# aber wir nutzen nur einen container + die app hat in ___ bereits den port definiert
EXPOSE 5000

# Command to run the app
CMD ["python3", "app.py"]



#sobald dockerignore steht, diesen befehl ins terminal, um das image zu bauen
# docker build -t  events-api .

#dann docker app starten:
# docker run -p 5000:5000 events-api

# app testen (separates Terminal!):
# docker ps
# pytest -v

#___

#um zu stoppen: ID raussuchen:
#"docker ps -a"

#remove container:
# "docker rm {id}"

#remove image:
#"docker rmi {image id}"
