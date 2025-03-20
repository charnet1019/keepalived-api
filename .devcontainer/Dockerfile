FROM python:3.12-alpine

# Install dependencies
RUN apk add --no-cache \
    bash \
    curl \
    git

# Install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
