FROM python

# stage 1

ARG BUILD_ENV=local

RUN apt-get update $$ apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./req .

RUN pip wheel --wheel-dir /usr/src/app/wheel \
    -r ${BUILD_ENV}.txt

# stage 2
FROM python
ARG BUILD_ENV=local
ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUILD_ENV=${BUILD_ENV}
WORKDIR ${APP_HOME}

RUN apt-get update $$ apt-get install --no-install-recommends -y \
    sudo git bash-completion nani ssh \
    libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgrupe --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 755 ${APP_HOME}/staticfiles
COPY --from=python /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh && \
    chmod +x /entrypoint.sh /start.sh

COPY --chown=django:django . ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint.sh"]

