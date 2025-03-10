<h1 align="center">BuddyBot</h1>

## Prerequisiti
- È necessario avere Docker installato (versione 27.3.1 o successiva) con BuildKit abilitato.

## Come abilitare BuildKit
Nel file config.json di Docker aggiungere la seguente opzione:
```
{
  "features": {
    "buildkit": true
  }
}
```
Il file si trova alla directory ~/.docker/config.json su Linux, C:\Users\<nome_utente>\.docker\config.json su Windows

## Come sfruttare il cache mount per ridurre il tempo di installazione delle dipendenze
- Creare un nuovo ambiente virtuale e attivarlo con:
  ```
  python -m venv nome_ambiente
  . nome_ambiente\scripts\activate
  ```
  su Windows;
  ```
  python3 -m venv nome_ambiente
  source nome_ambiente/bin/activate
  ```
  su Linux.
- Installare nell'ambiente virtuale le dipendenze principali contenute in primary_requirements.
- Creare un file con tutte le dipendenze secondarie con le versioni precise con:
  ```
  pip freeze > requirements.txt
  ```
  Questo comando scrive sul file requirements.txt tutte le dipendenze contenute nell'ambiente virtuale, con la loro versione.
  Dovreste ottenere qualcosa di molto simile a quanto già presente nel file requirements.txt.

Alla prima costruzione del container Docker "compila" la cache con tutti i pacchetti necessari, alle build successive verranno semplicemente installati i pacchetti elencati in requirements.txt già presenti nella cache, riducendo il tempo di build.
Il comando pip freeze compila il file requirements.txt con tutte le dipendenze contenute nell'ambiente virtuale, quindi è importante installare nell'ambiente virtuale solo i pacchetti necessari per evitare di aumentare inutilmente il tempo di build.
Di conseguenza se bisogna aggiungere una dipendenza a primary_requirements è sufficiente installarla nell'ambiente virtuale e richiamare pip freeze per aggiungere le nuove dipendenze secondarie a requirements.txt.
Se una dipendenza di primary_requirements non è più necessaria: 
- bisogna toglierla dal file primary_requirements.txt, 
- installare pip-autoremove con 'pip install pip-autoremove'
- eseguire 'pip uninstall nome-dipendenza',
- eseguire 'pip-autoremove nome_dipendenza -y' per rimuovere eventuali sottodipendenze installate esclusivamente per quella dipendenza
- aggiornare requirements.txt con 'pip freeze > requirements.txt'


## Avvio del container
Per avviare il container la prima volta, e ogni volta che si eseguono modifiche nel codice sorgente, eseguire il comando:
```
docker compose up --build
```

Al termine eseguire il comando:
```
docker compose down
```

Per riavviare il container senza modifiche nel codice è sufficiente
```
docker compose up
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
