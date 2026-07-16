FROM python:3.11-slim

WORKDIR /app

# System libraries needed by opencv (used by YOLO)
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libxcb1 && rm -rf /var/lib/apt/lists/*

# Install lightweight CPU-only torch first (no GPU on free servers)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run the web server
EXPOSE 5000
CMD ["python", "app.py"]
