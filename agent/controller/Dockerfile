FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p data

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY app/ app/

ENV CTRL_LOG_LEVEL=info

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
