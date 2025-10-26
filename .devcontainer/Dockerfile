FROM python:3.12-trixie AS builder

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    xclip \
    unzip \
    procps \
    pgrep
RUN pip install uv
