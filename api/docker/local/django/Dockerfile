FROM docker.io/python3.14.5-slim-bookworm as python

# Stage 1: Build our dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \


COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels -r {BUILD_ENVIRONMENT}.txt

# Stage 2 : Run Stage

FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system django django && \
    mkdir -p {APP_HOME}/staticfiles &&
    chown django:django ${APP_HOME}/staticfiles && \
    chown 775 ${APP_HOME}/staticfiles

COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-catch-dir --no-index --find-links=/wheels/ /wheels/*   && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh
RUN chown +x /entrypoint.sh /start.sh

COPY --chown+django:django . ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint.sh"]
