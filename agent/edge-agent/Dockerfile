FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY app/ app/

ENV AGENT_K8S_IN_CLUSTER=true
ENV AGENT_LOG_LEVEL=info

CMD ["python", "-m", "app.main"]
