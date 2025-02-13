# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt dan install dependency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file proyek
COPY . .

# Expose port 5000 (default Flask)
EXPOSE 5000

# Jalankan API dari folder src/api
CMD ["python", "src/api/app.py"]
