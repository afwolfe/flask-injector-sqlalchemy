FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip \
    && apk --no-cache --update add curl dumb-init

RUN addgroup -g 10001 nonroot \
    && adduser -D nonroot -u 10000 -G nonroot

USER nonroot
WORKDIR /app

ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY --chown=nonroot:nonroot config.yml /app
COPY --chown=nonroot:nonroot /app /app/app


# define the port number the container should expose
EXPOSE 8080

ENTRYPOINT [ "/usr/bin/dumb-init", "--"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.wsgi:app"]