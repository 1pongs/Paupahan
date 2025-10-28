FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for building packages if needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy app
COPY . /app

EXPOSE 8000

CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
