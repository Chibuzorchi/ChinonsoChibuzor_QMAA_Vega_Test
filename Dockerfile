FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Run tests
CMD ["pytest", "-v", "--headed=false"] 