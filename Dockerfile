FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV TG_BOT_TOKEN='' \
    SAUCENAO_TOKEN='' \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the source code to the container
COPY . .
RUN uv sync --frozen --no-dev

# Start the application
CMD ["uv", "run", "python", "main.py"]
