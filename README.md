<h1 align="center">BuddyBot</h1>

Progetto didattico svolto dal gruppo SWEg Labs per il corso di Ingegneria del Software 2024-25 - Università di Padova, laurea triennale in Infromatica.  
Azienda proponente: [AzzurroDigitale](https://www.azzurrodigitale.com/)  
Capitolato: [C9 - BuddyBot](https://www.math.unipd.it/~tullio/IS-1/2024/Progetto/C9.pdf)  


## Installazione

### Installazione di Docker
Prima di procedere con l'installazione di *BuddyBot* è importante verificare che Docker sia installato sulla propria macchina e pronto all'uso.  
Per farlo, digitare nel terminale:
```
docker --version
```
Se la console fornisce come output un numero di versione (ad esempio "Docker version 27.3.1, build ce12230"), allora Docker è correttamente installato e funzionante.  
Nel caso in cui il terminale segnali un errore, è possibile scaricare Docker seguendo la guida presente al link [https://docs.docker.com/get-started/get-docker/](https://docs.docker.com/get-started/get-docker/).  
Il gruppo *SWEg Labs* ha testato l'applicazione utilizzando Docker in versione 27.3.1, dunque si consiglia di utilizzare una versione uguale o superiore per garantire il corretto funzionamento dell'applicazione.

### Download dell'Applicazione
È possibile clonare la repository *GitHub* di BuddyBot eseguendo sul proprio terminale:
```
git clone https://github.com/SWEg-Labs/BuddyBot.git
```
Una volta scaricato il repository, posizionarsi nella cartella del progetto con il comando:
```
cd BuddyBot
```

### Creazione e configurazione del file `.env`
Tutte le variabili di sistema di configurazione sono già incluse nel *Dockerfile*.  
Tuttavia, per le impostazioni sensibili e personalizzabili, occorre creare nella directory `src/backend` un file `.env` contenente le seguenti voci (adattandole alle proprie esigenze):
```
OPENAI_API_KEY = la_tua_chiave_openai
OPENAI_MODEL_NAME = modello_llm_scelto

GITHUB_TOKEN = il_tuo_token_github
OWNER = proprietario_repository
REPO = nome_repository

ATLASSIAN_TOKEN = il_tuo_token_atlassian
ATLASSIAN_USER_EMAIL = la_tua_mail_atlassian

JIRA_BASE_URL = url_base_jira
JIRA_PROJECT_KEY = jira_project_key

CONFLUENCE_BASE_URL = confluence_base_key
CONFLUENCE_SPACE_KEY = confluence_space_key
```

### Creazione dell'immagine e avvio del container
Una volta pronti, è possibile creare l'immagine Docker posizionandosi nella cartella del progetto ed eseguendo:
```
docker compose up --build
```
La creazione dell'immagine impiegherà poco più di 5 minuti.  
Al termine della creazione di quest'ultima, verrà creato ed avviato il container `buddybot`. Al termine dell'utilizzo, per spegnere l'applicazione è possibile fermare il container impartendo la combinazione di tasti `Ctrl+C` nel terminale, oppure premendo il tasto Stop nell'applicazione *Docker Desktop*.  
Per i successivi accessi, aprire *Docker Desktop* e premere il tasto Play sul container `buddybot` per avviare di nuovo il container dell'applicazione. Per stopparlo, premere il tasto Stop dalla stessa interfaccia.  
Se si vuole continuare ad interagire da terminale con il container, è possibile eseguire il comando:
```
docker compose up
```
per avviarlo, e poi, come sopra, `Ctrl+C` per stopparlo.

### Esecuzione dell'Applicazione
Per avviare BuddyBot, è sufficiente aprire un *browser* e digitare nella barra degli indirizzi:
```
localhost:4200
```
Si aprirà dunque l'interfaccia grafica dell'applicazione web, pronta per ricevere domande dalla barra di input visibile nella parte inferiore dello schermo.  
Le istruzioni per l'utilizzo dell'applicazione sono fornite nel documento [Manuale Utente](https://sweg-labs.github.io/Documentazione/output/PB/Documentazione%20esterna/manuale_utente_v1.0.0.pdf).



## Come velocizzare la creazione dell'immagine Docker

### Come abilitare BuildKit
Nel file config.json di Docker aggiungere la seguente opzione:
```
{
  "features": {
    "buildkit": "true"
  }
}
```
Il file si trova alla directory ~/.docker/config.json su Linux, C:\Users\<nome_utente>\.docker\config.json su Windows

### Come sfruttare il cache mount per ridurre il tempo di installazione delle dipendenze
- Creare un nuovo ambiente virtuale e attivarlo con:
  ```
  python -m venv nome_ambiente
  nome_ambiente\scripts\activate
  ```
  su Windows;
  ```
  python3 -m venv nome_ambiente
  source nome_ambiente/bin/activate
  ```
  su Linux e macOS.
- Installare nell'ambiente virtuale le dipendenze principali contenute in *primary_requirements.txt*:
  ```
  pip install -r primary_requirements.txt
  ```
- Creare un file con tutte le dipendenze secondarie con le versioni precise con:
  ```
  pip freeze > requirements.txt
  ```
  Questo comando scrive sul file requirements.txt tutte le dipendenze contenute nell'ambiente virtuale, con la loro versione.  
  Dovreste ottenere qualcosa di molto simile a quanto già presente nel file requirements.txt.

Alla prima costruzione del container Docker "compila" la cache con tutti i pacchetti necessari, alle build successive verranno semplicemente installati i pacchetti elencati in requirements.txt già presenti nella cache, riducendo il tempo di build.  
Il comando `pip freeze` compila il file requirements.txt con tutte le dipendenze contenute nell'ambiente virtuale, quindi è importante installare nell'ambiente virtuale solo i pacchetti necessari per evitare di aumentare inutilmente il tempo di build.  
Di conseguenza se bisogna aggiungere una dipendenza a primary_requirements è sufficiente installarla nell'ambiente virtuale e richiamare `pip freeze` per aggiungere le nuove dipendenze secondarie a requirements.txt. Infatti, `pip freeze` fa una sovrascrizione completa del file requirements.txt precedente, quindi lo restituisce aggiornato.
Se una dipendenza di primary_requirements non è più necessaria:  
- bisogna toglierla dal file primary_requirements.txt, 
- installare pip-autoremove con `pip install pip-autoremove`,
- eseguire `pip uninstall nome-dipendenza`,
- eseguire `pip-autoremove nome_dipendenza -y` per rimuovere eventuali sottodipendenze installate esclusivamente per quella dipendenza,
- aggiornare requirements.txt con `pip freeze > requirements.txt`



## Aggiornamento automatico dei documenti

Esistono due file che registrano l'attività di aggiornamento automatico del cron:
- *src/backend/logs_db_update.txt*: per informazioni consuntive sugli aggiornamenti terminati.
- */var/log/cron.log*: per informazioni di monitoraggio sulle attività del cron, cioè vengono registrati i log lanciati dallo script che esegue l'aggiornamento automatico.

### Come visualizzare il file `logs_db_update.txt`
È possibile visualizzare il contenuto del file `logs_db_update.txt` seguendo i passaggi riportati di seguito:
1. Eseguire l'applicativo BuddyBot mediante Docker, come descritto nella sezione **Installazione** qui sopra.
2. Tramite Docker Desktop, accedere al container denominato `buddybot-backend`.
3. Recarsi nella sezione **Exec** del container.
4. Eseguire il comando:
  ```
  cat logs_db_update.txt
  ```
5. Se il container è stato appena creato, inizialmente il file sarà vuoto. Attendere qualche minuto e riprovare.

### Come visualizzare il file `cron.log`
È possibile visualizzare il contenuto del file `cron.log` seguendo i passaggi riportati di seguito:
1. Eseguire l'applicativo BuddyBot mediante Docker, come descritto nella sezione **Installazione** qui sopra.
2. Tramite Docker Desktop, accedere al container denominato `buddybot-backend`.
3. Recarsi nella sezione **Exec** del container.
4. Eseguire il comando:
  ```
  cat /var/log/cron.log
  ```
5. Se il container è stato appena creato, inizialmente il file non esisterà. Attendere qualche minuto e riprovare. Poiché il file viene scritto progressivamente durante l'esecuzione del cron, è possibile visualizzare un'istantanea di quanto scritto fino all'esatto momento in cui si è premuto Invio. Riprovando ad eseguire `cat` dopo qualche minuto, si potrà visualizzare la segnalazione di fine aggiornamento.

Per entrambi i file, se si vuole accedere al terminale del container `buddybot-backend` senza usare l'interfaccia grafica ed il limitato terminale di Docker Desktop, è possibile utilizzare il terminale del proprio sistema operativo digitandovi:
  ```
  docker exec -it buddybot-backend /bin/bash
  ```
Diventa a questo punto possibile visualizzare i due file log con gli stessi comandi `cat` descritti sopra.

### Come cambiare la frequenza di aggiornamento automatico
Attualmente il cron aggiorna i documenti ogni 20 minuti, e, nel caso un aggiornamento fallisca perchè viene lanciata un'eccezione, viene incrementata la frequenza a 15 minuti per massimo 3 tentativi di *retry*, per poi tornare alla frequenza normale in caso di successo o in caso venga superato il numero massimo di retry. E' possibile cambiare la frequenza di aggiornamento seguendo i passaggi riportati di seguito:
1. Recarsi dentro *src/backend*
2. Aprire il file `Dockerfile`
3. Cercare le seguenti righe:
  ```
  ENV DB_UPDATE_MAX_RETRIES=3
  ENV DB_UPDATE_FREQUENCY="*/20 * * * *" 
  ENV DB_UPDATE_ERROR_FREQUENCY="*/15 * * * *"
  ```
4. Se si desidera impostare l'aggiornamento automatico ogni 24 ore, e svolgere un retry dopo 1 ora in caso di fallimento, con massimo numero di retry pari a 5, modificare le suddette righe nel seguente modo:
  ```
  ENV DB_UPDATE_MAX_RETRIES=5
  ENV DB_UPDATE_FREQUENCY="*/1440 * * * *" 
  ENV DB_UPDATE_ERROR_FREQUENCY="*/60 * * * *"
  ```
Bisogna dunque convertire il valore temporale desiderato in minuti.
5. Ricreare l'immagine Docker come spiegato nella sezione **Installazione**.



## Come eseguire BuddyBot senza Docker Compose
Nel caso si desideri eseguire BuddyBot al di fuori del container creato con Docker Compose, come risulta molto comodo fare soprattutto in fase di sviluppo, seguire i passaggi qui riportati:
1. Installare Python dal seguente link: https://www.python.org/downloads/
2. Installare Angular dal seguente link: https://angular.dev/installation
2. Installare PostgreSQL dal seguente link: https://www.postgresql.org/download/
3. Se si desidera un'interfaccia grafica per la gestione del database di Postgres, installare *pgAdmin 4* dal seguente link: https://www.pgadmin.org/download/
4. In Postgres, creare uno user `buddybot`, con password `buddybot`, e un database di nome `buddybot`
5. Scaricare l'immagine di Chroma dal *Docker Hub*:
  ```
  docker pull chromadb/chroma
  ```
6. Avviare un container da tale immagine:
  ```
  docker run -d --name chromadb -p 8000:8000 chromadb/chroma
  ```
Dopo la creazione, il container sarà visualizzabile e gestibile tramite l'applicazione *Docker Desktop*.
7. Aggiungere in fondo al file `.env` già creato nella sezione **Installazione** le seguenti voci:
  ```
  CHROMA_HOST=localhost
  CHROMA_PORT=8000

  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  POSTGRES_USER=buddybot
  POSTGRES_PASSWORD=buddybot
  POSTGRES_DB_NAME=buddybot

  LOGGING_ENABLED=true
  TIMEOUT=10
  DB_UPDATE_ERROR='0'
  DB_UPDATE_RETRY='2'
  DB_UPDATE_MAX_RETRIES=3
  DB_UPDATE_FREQUENCY=*/10 * * * *
  DB_UPDATE_ERROR_FREQUENCY=*/5 * * * *

  CRONTAB_PATH=/etc/cron.d/crontab
  CRONJOB_COMMAND=/usr/local/bin/python /backend/vector_store_update_controller.py >> /var/log/cron.log
  ```
8. Recarsi su *src/backend*, aprire il file  `vector_store_update_controller.py` e cercare le seguenti righe:
  ```
  # Inizializza cron
  cron = CronTab(tabfile=crontab_path)
  # cron = CronTab(user=True)   # Per caricare i documenti manualmente
  ```
9. Commentare la prima riga di inizializzazione del cron e decommentare la seconda:
  ```
  # Inizializza cron
  # cron = CronTab(tabfile=crontab_path)
  cron = CronTab(user=True)   # Per caricare i documenti manualmente
  ```
10. Dopo essersi assicurati che il container di Chroma sia attivo, nel terminale, recarsi nella cartella *src/backend*, ed eseguire:
  ```
  python vector_store_update_controller.py
  ```
Questo script, dovesse andare a buon fine, in una decina di minuti aggiornerà il database vettoriale Chroma hostato sul container a parte creato sopra  
11. Invertire i punti 7 e 9 di questa lista, cioè tornare al vecchio file `.env` e al vecchio file `vector_store_update_controller.py`  
12. Aprire un nuovo terminale, accedere ancora alla cartella *src/backend*, ed eseguire questo comando per creare un nuovo ambiente virtuale:
  ```
  python -m venv nome_ambiente
  ```
13. Attivare l'ambiente virtuale:
  ```
  nome_ambiente\scripts\activate
  ```
  su Windows;
  ```
  source nome_ambiente/bin/activate
  ```
  su Linux e macOS.  
14. Installare le dipendenze nell'ambiente virtuale:
  ```
  pip install -r primary_requirements.txt
  ```
15. Avviare il backend di BuddyBot:
  ```
  python app.py
  ```
16. Aprire un nuovo terminale, accedere alla cartella *src/frontend*, ed eseguire questo comando per avviare il frontend di BuddyBot
  ```
  ng serve
  ```
17. Aprire un browser ed accedere all'indirizzo
  ```
  localhost:4200
  ```
E' ora possibile utilizzare BuddyBot senza usufruire di Docker Compose.  
In caso si facciano sviluppi nel backend, è necessario impartire `Ctrl+C` nel terminale su cui era stato avviato `app.py`, e riavviarlo subito dopo.  
In caso si facciano sviluppi nel frontend, non ci sono problemi poichè Angular aggiorna la pagina in tempo reale.



## Come eseguire i test sul codice di BuddyBot
BuddyBot è stato testato con test di unità e test di integrazione, sia lato backend sia lato frontend, raggiungendo in entrambi i casi una coverage delle righe di codice pari al 90%, quindi superiore alla soglia minima del 75% concordata con il proponente.  
I test del backend sono disponibili dentro la cartella *tests*, suddivisi in test di unità e test di integrazione.  
I test del frontend, invece, sono distribuiti in vari file situati accanto al codice sorgente che si sta testando, com'è caratteristico dei progetti Angular. Accedendo a *src/frontend/src/app/chat* e, all'interno delle cartelle dedicate a ciascun componente, dentro i file con estensione `.spec.ts`, si possono visualizzare i test di integrazione e test di unità per quel componente, suddivisi in blocchi `describe` dedicati.

### Come eseguire i test del backend
1. Se non si ha già creato un ambiente virtuale Python, crearlo seguendo i punti 12, 13 e 14 della sezione **Come eseguire BuddyBot senza Docker Compose**, e, al termine, tornare nella root del progetto con:
  ```
  cd ../..
  ```
2. Eseguire il seguente comando per avviare i test:
  ```
  pytest
  ```
Sul terminale verrà visualizzato l'esito dei test e la coverage delle righe raggiunta.  
Se si desidera sviluppare nuovi test, in caso uno di questi fallisca, è possibile visualizzare un output più esaustivo dell'errore eseguendo:
  ```
  pytest -vv
  ```

### Come eseguire i test del frontend
1. Da terminale, accedere alla cartella *src/frontend*
2. Eseguire il seguente comando per avviare i test:
  ```
  ng test
  ```
Si aprirà una finestra di browser in cui verrà visualizzato l'esito dei test svolti, la loro descrizione e la loro classificazione (componente testato e tipo di test (unità o integrazione)).  
Sul terminale, rimasto attivo, apparirà la coverage raggiunta: per il progetto didattico è stata presa in considerazione solo la coverage delle righe, cioè l'ultima visualizzata.  
Per chiudere la finestra del browser, non è possibile cliccare la "X" in alto a destra, poichè così facendo verrà poi ricreata automaticamente una nuova finestra; occorre invece impartire `Ctrl+C` nel terminale, e ciò chiuderà l'ambiente di test di Angular. Tuttavia, è possibile anche tenerlo attivo, poichè, così facendo, nel caso venga sviluppato un nuovo test, esso verrà eseguito in tempo reale senza dover reimpartire alcun comando.  
