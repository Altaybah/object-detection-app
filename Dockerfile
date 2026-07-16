FROM python:3.11-slim

# Create the working directory
WORKDIR /app

# Install system libraries that opencv (used by YOLO) needs
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run the web server
EXPOSE 5000
CMD ["python", "app.py"]