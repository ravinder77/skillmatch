# ===============================
# 1️⃣ Base image
# ===============================
FROM python:3.14-slim AS base

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# ===============================
# 3️⃣ Install Python dependencies
# ===============================
COPY requirements.txt .

# Force clean, cache-free dependency install
RUN uv sync --no-cache

# ===============================
# 4️⃣ Copy app source
# ===============================
COPY . .

# ===============================
# 5️⃣ Expose port and set command
# ===============================
EXPOSE 8000

# Default startup command (development mode)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
