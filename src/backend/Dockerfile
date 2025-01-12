FROM python:latest

# Argomenti e variabili di configurazione
ARG WORKDIR="/backend"
ARG SRC_DIRECTORY="."
ENV REQUIREMENTS_PATH="${WORKDIR}/requirements.txt"
ENV DOTENV_PATH="${WORKDIR}/env"

ARG DB_UPDATE_PATH="${WORKDIR}/db_update_controller.py"
ARG CRON_LOG_PATH="/var/log/cron.log"
ARG PYTHON_INTERPRETER_PATH="/usr/local/bin/python"
ENV CRONTAB_PATH="/etc/cron.d/crontab"
ENV CRONJOB_COMMAND="${PYTHON_INTERPRETER_PATH} ${DB_UPDATE_PATH} >> ${CRON_LOG_PATH}"

ENV LOGGING_ENABLED=true
ENV TIMEOUT=10
ENV DB_UPDATE_MAX_RETRIES=3
ENV DB_UPDATE_FREQUENCY="*/10 * * * *" 
ENV DB_UPDATE_ERROR_FREQUENCY="*/5 * * * *"
ENV DB_UPDATE_ERROR='0'
ENV DB_UPDATE_RETRY='0'

# Setta working directory
WORKDIR ${WORKDIR}

# Copia codice sorgente nella working directory
COPY ${SRC_DIRECTORY} ${WORKDIR}

# Installa dipendenze
RUN pip install -r $REQUIREMENTS_PATH && \
    apt-get update && apt-get install -y cron

# Copia le variabili necessarie nel .env    (#altrimenti lo script chiamato dal cronjob non le vede)
RUN echo "" >> ${DOTENV_PATH} && \
    echo "LOGGING_ENABLED=${LOGGING_ENABLED}" >> ${DOTENV_PATH} && \
    echo "TIMEOUT=${TIMEOUT}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_ERROR=${DB_UPDATE_ERROR}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_RETRY=${DB_UPDATE_RETRY}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_MAX_RETRIES=${DB_UPDATE_MAX_RETRIES}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_FREQUENCY=${DB_UPDATE_FREQUENCY}" >> ${DOTENV_PATH} && \
    echo "DB_UPDATE_ERROR_FREQUENCY=${DB_UPDATE_ERROR_FREQUENCY}" >> ${DOTENV_PATH} && \
    echo "CRONTAB_PATH=${CRONTAB_PATH}" >> ${DOTENV_PATH} && \
    echo "CRONJOB_COMMAND=${CRONJOB_COMMAND}" >> ${DOTENV_PATH}
    
# Crea il file crontab, inserisce il comando e gli assegna i permessi necessari
RUN echo "${DB_UPDATE_FREQUENCY} root ${CRONJOB_COMMAND}" > ${CRONTAB_PATH} && \
    chmod 0644 ${CRONTAB_PATH}

CMD ["python", "app.py"]
