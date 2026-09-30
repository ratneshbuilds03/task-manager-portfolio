FROM python:3.14.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY run.py .
RUN addgroup --system app && adduser --system --ingroup app app \
    && chown -R app:app /app

USER app
EXPOSE 5000
CMD ["python", "run.py"]