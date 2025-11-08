FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

WORKDIR /App

ARG DEV=false

# copy only requirements first (cache-friendly)
COPY requirements.txt requirements.dev.txt /App/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /App/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
      pip install --no-cache-dir -r /App/requirements.dev.txt; \
    fi

# copy the application code (explicitly copy host ./App into container /App)
COPY ./App /App

# create non-root user and give ownership of /App
RUN useradd --create-home --shell /bin/sh django-user && \
    chown -R django-user:django-user /App

USER django-user

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
