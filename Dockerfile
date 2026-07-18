FROM python:3.11-slim

WORKDIR /app

#Install small system tools that the detection library needs to handle images
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libxcb1 && rm -rf /var/lib/apt/lists/*

#Install lightweight CPU-only torch first because the free server has no GPU anyway
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files - app.py, best.pt....-
COPY . .

# Run the web server
EXPOSE 5000
CMD ["python", "app.py"]
