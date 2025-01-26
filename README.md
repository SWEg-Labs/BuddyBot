<h1 align="center">BuddyBot</h1>

## Prerequisiti
- È necessario avere Docker installato

## Avvio del container
Per avviare il container eseguire il comando:
```
docker compose up --build
```

Al termine eseguire il comando:
```
docker compose down
```

## Esecuzione dell'applicazione da terminale
- Andare nel terminale del container
  - Tra i Containers di Docker Desktop, selezionare "backend"
  - Una volta entrati nel container andare alla voce "Exec"
- Eseguire:
  ```
  python backend/main.py
  ```
- Se attendete da 2 a 5 minuti dall'inizio di un minuto che finisce per 0 (es.: 10:40, 16:30, 14:10) ed inserite nel chatBot il comando "v" per vedere i documenti presenti nel database, vedrete che il database non è vuoto.
- E' possibile visionare i log dell'aggiornamento uscendo dall'app con "exit" e digitando nel container:
  ```
  cat /var/log/cron.log
  ```
- L'aggiornamento verrà effettuato ogni 10 minuti, cioè inizierà in ogni minuto che finisce per 0, per avere il database vettoriale sempre aggiornato!
Piccola nota: dovesse essere eliminato un documento in una delle piattaforme collegate, nel database vettoriale esso non verrebbe eliminato.

In alternativa dal terminale della macchina si può eseguire: 
```
docker exec -it buddybot-backend /bin/bash
 ```
Per accedere al terminale del container chiamato buddybot-backend.


## Esecuzione dell'applicazione da browser

E' sufficiente aprire un browser e digitare:
```
localhost:4200
```
Per accedere all'interfaccia grafica di BuddyBot.

Una volta lì, è possibile o caricare i file nel database vettoriale utilizzando i pulsanti appositi,
oppure aspettare 10 minuti e lasciare che vengano caricati in automatico.

Una volta caricati, sarà dunque possibile porre domande nell'apposita barra e ricevere risposte nel riquadro sovrastante.


## .env
Tutte le variabili di sistema di configurazione sono nel dockerfile.
Nel .env servono solo le sequenti voci:
```
OPENAI_API_KEY = la_tua_chiave_openai
OPENAI_MODEL_NAME = modello_llm_scelto
CHROMA_HOST = host_database
CHROMA_PORT = porta_database
GITHUB_TOKEN = il_tuo_token_github
OWNER = owner_repository
REPO = nome_repository
ATLASSIAN_TOKEN = il_tuo_token_atlassian
ATLASSIAN_USER_EMAIL = la_tua_mail_atlassian
JIRA_BASE_URL= url_base_jira
JIRA_PROJECT_KEY= jira_project_key
CONFLUENCE_BASE_URL= confluence_base_key
CONFLUENCE_SPACE_KEY= confluence_space_key
```
Inserire il .env nella directory src/backend.
