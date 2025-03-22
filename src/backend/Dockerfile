FROM python:3.13.1

# Argomenti e variabili di configurazione
ARG WORKDIR="/backend"
ARG SRC_DIRECTORY="."
ENV REQUIREMENTS_PATH="${WORKDIR}/requirements.txt"
ENV DOTENV_PATH="${WORKDIR}/.env"

ARG CHROMA_HOST="chroma-db"
ARG CHROMA_PORT="8000"

ARG POSTGRES_HOST="postgres-db"
ARG POSTGRES_PORT="5432"
ARG POSTGRES_USER="buddybot"
ARG POSTGRES_PASSWORD="buddybot"
ARG POSTGRES_DB_NAME="buddybot"

ARG DB_UPDATE_PATH="${WORKDIR}/vector_store_update_controller.py"
ARG CRON_LOG_PATH="/var/log/cron.log"
ARG PYTHON_INTERPRETER_PATH="/usr/local/bin/python"
ENV CRONTAB_PATH="/etc/cron.d/crontab"
ENV CRONJOB_COMMAND="${PYTHON_INTERPRETER_PATH} ${DB_UPDATE_PATH} >> ${CRON_LOG_PATH}"

ENV SUPERVISOR_CONF_PATH="/etc/supervisor/supervisord.conf"

ENV LOGGING_ENABLED=true
ENV LOG_FILE_PATH="${WORKDIR}/logs_db_update.txt"
ENV REQUESTS_TIMEOUT=10
ENV DB_UPDATE_MAX_RETRIES=3
ENV DB_UPDATE_FREQUENCY="*/20 * * * *" 
ENV DB_UPDATE_ERROR_FREQUENCY="*/15 * * * *"
ENV DB_UPDATE_ERROR='0'
ENV DB_UPDATE_RETRY='0'

# Setta working directory
WORKDIR ${WORKDIR}

# Copia codice sorgente nella working directory
COPY ${SRC_DIRECTORY} ${WORKDIR}

# Installa dipendenze e supervisord
RUN apt-get update && apt-get install -y cron supervisor 
RUN --mount=type=cache,target=/root/.cache/pip pip install -r $REQUIREMENTS_PATH

# Copia le variabili necessarie nel .env (altrimenti lo script chiamato dal cronjob non le vede)
RUN echo "" >> ${DOTENV_PATH} && \
    echo "CHROMA_HOST=${CHROMA_HOST}" >> ${DOTENV_PATH} && \
    echo "CHROMA_PORT=${CHROMA_PORT}" >> ${DOTENV_PATH} && \
    echo "" >> ${DOTENV_PATH} && \
    echo "POSTGRES_HOST=${POSTGRES_HOST}" >> ${DOTENV_PATH} && \
    echo "POSTGRES_PORT=${POSTGRES_PORT}" >> ${DOTENV_PATH} && \
    echo "POSTGRES_USER=${POSTGRES_USER}" >> ${DOTENV_PATH} && \
    echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> ${DOTENV_PATH} && \
    echo "POSTGRES_DB_NAME=${POSTGRES_DB_NAME}" >> ${DOTENV_PATH} && \
    echo "" >> ${DOTENV_PATH} && \
    echo "LOGGING_ENABLED=${LOGGING_ENABLED}" >> ${DOTENV_PATH} && \
    echo "LOG_FILE_PATH=${LOG_FILE_PATH}" >> ${DOTENV_PATH} && \
    echo "" >> ${DOTENV_PATH} && \
    echo "REQUESTS_TIMEOUT=${REQUESTS_TIMEOUT}" >> ${DOTENV_PATH} && \
    echo "" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_ERROR=${DB_UPDATE_ERROR}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_RETRY=${DB_UPDATE_RETRY}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_MAX_RETRIES=${DB_UPDATE_MAX_RETRIES}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_FREQUENCY=${DB_UPDATE_FREQUENCY}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_ERROR_FREQUENCY=${DB_UPDATE_ERROR_FREQUENCY}" >> ${DOTENV_PATH} && \
    echo "" >> ${DOTENV_PATH} && \
    echo "CRONTAB_PATH=${CRONTAB_PATH}" >> ${DOTENV_PATH} && \
    echo "CRONJOB_COMMAND=${CRONJOB_COMMAND}" >> ${DOTENV_PATH}

# Crea il file crontab, inserisce il comando e gli assegna i permessi necessari
RUN echo "${DB_UPDATE_FREQUENCY} root ${CRONJOB_COMMAND}" > ${CRONTAB_PATH} && \
    chmod 0644 ${CRONTAB_PATH}

# Crea dinamicamente il file di configurazione di supervisord
RUN echo "[supervisord]" > ${SUPERVISOR_CONF_PATH} && \
    echo "nodaemon=true" >> ${SUPERVISOR_CONF_PATH} && \
    echo "" >> ${SUPERVISOR_CONF_PATH} && \
    echo "[program:cron]" >> ${SUPERVISOR_CONF_PATH} && \
    echo "command=cron -f" >> ${SUPERVISOR_CONF_PATH} && \
    echo "autostart=true" >> ${SUPERVISOR_CONF_PATH} && \
    echo "autorestart=true" >> ${SUPERVISOR_CONF_PATH} && \
    echo "" >> ${SUPERVISOR_CONF_PATH} && \
    echo "[program:fastapi]" >> ${SUPERVISOR_CONF_PATH} && \
    echo "command=python ${WORKDIR}/app.py" >> ${SUPERVISOR_CONF_PATH} && \
    echo "autostart=true" >> ${SUPERVISOR_CONF_PATH} && \
    echo "autorestart=true" >> ${SUPERVISOR_CONF_PATH}

# Usa supervisord come entrypoint
ENTRYPOINT ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
