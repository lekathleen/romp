# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN adduser --disabled-password --gecos "" romp

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh && chown -R romp:romp /app

USER romp

# Required for ECS to know when the container is ready to serve traffic
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]