FROM python:3.10-alpine3.18

LABEL maintainer=:"tamarammt"

ENV PYTHONUNBUFFERED 1 

# Copy code and requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./dev-requirements.txt /tmp/dev-requirements.txt
COPY ./project /project
WORKDIR /project
EXPOSE  8000

ARG DEV=false
# Create and activate virtual environment and Install development dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then \
        /venv/bin/pip install -r /tmp/dev-requirements.txt ; \
    fi && \
    rm -rf /tmp &&\
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Add project directory to PATH
ENV PATH="/venv/bin:$PATH"

USER django-user