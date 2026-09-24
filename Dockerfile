# 1. Use an official, lightweight Python runtime blueprint base
FROM python:3.11-slim

# 2. Set the internal container directory where our app code will live
WORKDIR /app

# 3. Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy over your requirements first to leverage Docker's build caching layer
COPY requirements.txt .

# 5. Upgrade pip and install all production application dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your local project files into the container's working directory
COPY . .

# 7. Expose the port FastAPI will stream traffic out of
EXPOSE 8000

# 8. Define the default runtime execution command to boot your Uvicorn live server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
