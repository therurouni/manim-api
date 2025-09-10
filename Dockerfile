FROM engineervix/python-latex:3.11-slim-bookworm

# Install system dependencies for Manim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    libffi-dev \
    dvisvgm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]