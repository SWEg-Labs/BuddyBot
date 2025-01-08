try:
    print("--------------------------------------------------")
    from datetime import datetime
    import sys
    
    # Stampa l'ora attuale
    print(f"[{datetime.now().strftime('%H:%M:%S')}]", end=" ")

    import os
    from dotenv import load_dotenv, set_key, find_dotenv
    load_dotenv()
    from controllers.userController import UserController
    from repositories.vectorStoreRepository import VectorStoreRepository
    from services.githubService import GithubService
    from services.jiraService import JiraService
    from services.confluenceService import ConfluenceService
    from crontab import CronTab

    env_path = find_dotenv()
    crontab_path = os.getenv('CRONTAB_PATH')
    cron_command = os.getenv('CRON_COMMAND')

    #stabilisce la frequenza dei tentativi di aggioranemnto del db in stato di errore e successo
    cronjob_error_frequency = '*/1 * * * *'
    cronjob_success_frequency = '*/5 * * * *'
    db_update_max_retries = 3

    #reindirizza lo stdout delle funzioni sotto per non farlo comparire nel log
    stdout_originale = sys.stdout   
    sys.stdout = open(os.devnull, 'w')
    
    # inizializza cron
    cron = CronTab(tabfile=crontab_path)
    # inizializza vector store
    vector_store = VectorStoreRepository()
    # inizializza github service
    github_service = GithubService()
    # inizializza jira service
    jira_service = JiraService()
    # inizializza confluence service
    confluence_service = ConfluenceService()
    # set args vector
    args = (vector_store, github_service, jira_service, confluence_service)
    # update database
    UserController._load_github_files(*args)
    UserController._load_github_commits(*args)
    UserController._load_jira(*args)
    UserController._load_confluence(*args)

    # Se siamo passati da stato di errore a stato di successo ripristina variabili e cron
    if os.getenv('DB_UPDATE_ERROR')=='1':
        set_key(env_path, 'DB_UPDATE_ERROR', '0')
        set_key(env_path, 'DB_UPDATE_RETRY', '0')
        iter = cron.find_command(cron_command)
        for job in iter:
            job.setall(cronjob_success_frequency)
        cron.write()

    # ripristina lo stdout
    sys.stdout = stdout_originale
    print("Aggiornamento completato")

except Exception as e:
    sys.stdout = stdout_originale
    print(f"Error: {e}")
    
    try:
        #Se siamo passati da stato di successo a stato di errore modifica variabil e cron
        if os.getenv('DB_UPDATE_ERROR')=='0':
            set_key(env_path, 'DB_UPDATE_ERROR', '1')
            set_key(env_path, 'DB_UPDATE_RETRY', '1')
            iter = cron.find_command(cron_command)
            for job in iter:
                job.setall(cronjob_error_frequency)
            cron.write()

        #Se siamo al terzo retry riporta cron alla normalità, continua a incrementare retry
        elif int(os.getenv('DB_UPDATE_RETRY'))>=db_update_max_retries:
            retry = os.getenv('DB_UPDATE_RETRY')
            set_key(env_path, 'DB_UPDATE_RETRY', str(int(retry)+1))
            iter = cron.find_command(cron_command)
            for job in iter:
                job.setall(cronjob_success_frequency)
            cron.write()

        # Altrimenti (eravamo già in stato di errore e non siamo ancora al terzo retry) incrementa contatore dei retry
        else:
            retry = os.getenv('DB_UPDATE_RETRY')
            set_key(env_path, 'DB_UPDATE_RETRY', str(int(retry)+1))

        # Se siamo oltre il terzo retry il cron è già stato portato alla normalità e sta riprovando ogni 5 minuti. Non fare nulla

    except Exception as e:
        print(f"Errore durante gestione errore: {e}")