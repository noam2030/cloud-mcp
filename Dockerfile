FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
# Install dependencies first so Docker can cache this layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY server.py ./

# Cloud Run sets PORT. Listen on all interfaces inside the container.
ENV HOST=0.0.0.0
CMD ["uv", "run", "--no-sync", "python", "server.py"]
