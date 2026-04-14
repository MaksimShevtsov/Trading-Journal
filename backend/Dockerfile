# Stage 1: Build
FROM python:3.12-slim AS builder

RUN pip install uv

WORKDIR /app

# Install dependencies first (layer-cached separately from app code)
COPY pyproject.toml .
# Stub app package so uv can resolve the project without the full source
RUN mkdir -p app && touch app/__init__.py && \
    uv pip install --system . && \
    rm -rf app

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
