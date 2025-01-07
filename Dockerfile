FROM python:latest

# Setta working directory
WORKDIR /app

# Copia codice sorgente nella working directory
COPY src/ /app

# Installa dipendenze
RUN pip install -r backend/requirements.txt

# Aggiorna repository e installa pacchetti necessari
RUN apt-get update && apt-get install -y cron

# Copia file cron.log
COPY cron.log /var/log/cron.log

# Copia file crontab
COPY crontab /etc/cron.d/crontab
# Assegna permessi necessari al file crontab
RUN chmod 0644 /etc/cron.d/crontab

# Espone porta 8000
EXPOSE 8000

# Avvia cron
ENTRYPOINT [ "cron", "-f" ]
