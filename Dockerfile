# Start from an official, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements file first (not the whole project yet)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model - needed for skill extraction
RUN python -m spacy download en_core_web_sm

# Now copy the rest of the project files
COPY . .

# Document which port the app listens on
EXPOSE 8000

# Command that runs when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]