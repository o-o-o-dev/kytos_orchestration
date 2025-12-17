FROM public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 AS aws-lambda-adapter

FROM ghcr.io/astral-sh/uv:latest AS uv

# Base image
FROM python:3.12-slim-bookworm AS base

WORKDIR /app
ENV TZ=Asia/Tokyo

COPY --from=aws-lambda-adapter /lambda-adapter /opt/extensions/lambda-adapter

# Build stage
FROM base AS builder

ENV UV_COMPILE_BYTECODE=1 \
  UV_NO_INSTALLER_METADATA=1 \
  UV_LINK_MODE=copy

RUN --mount=from=uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-dev

# Production stage
FROM base AS prod

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# NOTE: FastAPI CLIではなくuvicornを利用しています 
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080"]
