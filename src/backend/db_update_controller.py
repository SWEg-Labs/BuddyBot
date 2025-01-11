import os
from dotenv import load_dotenv, set_key, find_dotenv
load_dotenv()
from crontab import CronTab
from db_update import update_database
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    print("--------------------------------------------------")
    
    # Stampa l'ora di inizio aggiornamento
    italy_tz = ZoneInfo("Europe/Rome")
    start_italian_time = datetime.now(italy_tz)
    start_time_string = start_italian_time.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{start_time_string}] Inizio aggiornamento")

    env_path = find_dotenv()
    crontab_path = os.environ.get('CRONTAB_PATH')
    cron_command = os.getenv('CRONJOB_COMMAND')
    db_update_frequency = os.getenv('DB_UPDATE_FREQUENCY')
    db_update_error_frequency = os.getenv('DB_UPDATE_ERROR_FREQUENCY')
    db_update_max_retries = int(os.getenv('DB_UPDATE_MAX_RETRIES'))
    '''
    print(f"crontab_path: {crontab_path}")
    print(f"cron_command: {cron_command}")
    print(f"db_update_frequency: {db_update_frequency}")
    print(f"db_update_error_frequency: {db_update_error_frequency}")
    print(f"db_update_max_retries: {db_update_max_retries}")
    '''
    # inizializza cron
    cron = CronTab(tabfile=crontab_path)

    # Esegue l'aggiornamento del database
    update_database()

    # Se siamo passati da stato di errore a stato di successo ripristina variabili e cron
    if os.getenv('DB_UPDATE_ERROR')=='1':
        '''
        print(f"db_update_error prima: {os.getenv('DB_UPDATE_ERROR')}")
        print(f"db_update_retry prima: {os.getenv('DB_UPDATE_RETRY')}")
        print("errore->successo")
        '''
        set_key(env_path, 'DB_UPDATE_ERROR', '0')
        set_key(env_path, 'DB_UPDATE_RETRY', '0')
        iter = cron.find_command(cron_command)
        for job in iter:
            '''print(f"job: {job}")'''
            job.setall(db_update_frequency)
        cron.write()

    # Stampa l'ora di fine aggiornamento
    end_italian_time = datetime.now(italy_tz)
    end_time_string = end_italian_time.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{end_time_string}] Aggiornamento completato")

except Exception as e:
    print(f"Error: {e}")

    try:
        # Se siamo passati da stato di successo a stato di errore modifica variabil e cron
        if os.getenv('DB_UPDATE_ERROR')=='0':
            '''
            print(f"db_update_error prima: {os.getenv('DB_UPDATE_ERROR')}")
            print(f"db_update_retry prima: {os.getenv('DB_UPDATE_RETRY')}")
            print("successo->errore")
            '''
            set_key(env_path, 'DB_UPDATE_ERROR', '1')
            set_key(env_path, 'DB_UPDATE_RETRY', '1')
            iter = cron.find_command(cron_command)
            for job in iter:
                '''print(f"job: {job}")'''
                job.setall(db_update_error_frequency)
            cron.write()

        # Se siamo al terzo retry riporta cron alla normalità, continua a incrementare retry
        elif int(os.getenv('DB_UPDATE_RETRY'))>=db_update_max_retries:
            '''
            print(f"db_update_error prima: {os.getenv('DB_UPDATE_ERROR')}")
            print(f"db_update_retry prima: {os.getenv('DB_UPDATE_RETRY')}")
            print("terzo retry o più")
            '''
            retry = os.getenv('DB_UPDATE_RETRY')
            set_key(env_path, 'DB_UPDATE_RETRY', str(int(retry)+1))
            iter = cron.find_command(cron_command)
            for job in iter:
                '''print(f"job: {job}")'''
                job.setall(db_update_frequency)
            cron.write()

        # Altrimenti (eravamo già in stato di errore e non siamo ancora al terzo retry) incrementa contatore dei retry
        else:
            '''
            print(f"db_update_error prima: {os.getenv('DB_UPDATE_ERROR')}")
            print(f"db_update_retry prima: {os.getenv('DB_UPDATE_RETRY')}")
            print("incremento retry")
            '''
            retry = os.getenv('DB_UPDATE_RETRY')
            set_key(env_path, 'DB_UPDATE_RETRY', str(int(retry)+1))

        # Se siamo oltre il terzo retry il cron è già stato portato alla normalità e sta riprovando ogni 5 minuti. Non fare nulla

    except Exception as e2:
        print(f"Errore durante gestione errore: {e2}")

finally:
    print("--------------------------------------------------")
