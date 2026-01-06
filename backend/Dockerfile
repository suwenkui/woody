# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements from the build context (which should be the project root)
COPY backend/requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into /app/backend
COPY backend ./backend

# Expose port
EXPOSE 8000

# Run from /app, so 'backend' is a package
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
