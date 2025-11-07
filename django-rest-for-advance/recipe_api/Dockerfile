FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

WORKDIR /App

ARG DEV=false

COPY requirements.txt .
COPY requirements.dev.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        pip install --no-cache-dir -r requirements.dev.txt; \
    fi

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

USER django-user