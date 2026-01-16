# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (for better Docker layer caching)
COPY pyproject.toml uv.lock ./

# Sync dependencies using uv (creates virtual environment and installs packages)
RUN uv sync --frozen --no-dev

# Copy application code
COPY main.py ./

# Set environment variable for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Run Streamlit using uv run (executes in the uv-managed virtual environment)
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]