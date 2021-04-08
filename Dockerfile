##################
# BASE BUILD LAYER
##################
FROM python:3.9-slim AS base

ENV PYTHONUNBUFFERED 1

# ensures python output is sent straight to terminal
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file/59812588
WORKDIR /app

COPY requirements.txt ./

RUN python3 -m pip install -U pip && \
    pip3 install --no-cache-dir -r requirements.txt

##################
# TEST BUILD LAYER
##################
FROM base AS test

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends build-essential

COPY . .

CMD echo "COMPLETE"

##################
# PROD BUILD LAYER
##################
# FROM base AS prod

# COPY . .

# Put custom command here. Don't forget to change "command" in docker-compose.yml
# CMD python manage.py runserver 0.0.0.0:8000