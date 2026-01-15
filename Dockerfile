# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock main.py ./

# Install uv + all dependencies
RUN pip install "uv[all]"

# Set environment variable for Cloud Run
ENV PORT 8080
EXPOSE 8080

# Run Streamlit with proper host and port
CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0", "--server.headless", "true"]
