FROM python:3.10-alpine3.18

LABEL maintainer=:"tamarammt"

ENV PYTHONUNBUFFERED 1 

# Copy code and requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./project /project
WORKDIR /project
EXPOSE  8000

# Create and activate virtual environment and Install development dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp &&\
    apk del .tmp-build-deps 

RUN adduser --system --no-create-home --shell /bin/bash appuser

USER appuser

# Add project directory to PATH
ENV PATH="/venv/bin:$PATH"

