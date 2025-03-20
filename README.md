<h1 align="center">BuddyBot</h1>

Progetto didattico svolto dal gruppo SWEg Labs per il corso di Ingegneria del Software - Università di Padova, 2024-25.  
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
Nel caso in cui il terminale segnali un errore, è possibile scaricare Docker seguendo la guida presente al link [https://docs.docker.com/get-started/get-docker/](https://docs.docker.com/get-started/get-docker/) *(Ultimo accesso: 03/04/2025)*.  
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
Al termine della creazione di quest'ultima, verrà creato ed avviato il container `buddybot`. Al termine dell'utilizzo, per spegnere l'applicazione è possibile fermare il container con la combinazione di tasti `Ctrl+C`.  
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
Di conseguenza se bisogna aggiungere una dipendenza a primary_requirements è sufficiente installarla nell'ambiente virtuale e richiamare pip freeze per aggiungere le nuove dipendenze secondarie a requirements.txt. Infatti, pip freeze fa una sovrascrizione completa del file requirements precedente, quindi lo restituisce aggiornato.
Se una dipendenza di primary_requirements non è più necessaria: 
- bisogna toglierla dal file primary_requirements.txt, 
- installare pip-autoremove con 'pip install pip-autoremove'
- eseguire 'pip uninstall nome-dipendenza',
- eseguire 'pip-autoremove nome_dipendenza -y' per rimuovere eventuali sottodipendenze installate esclusivamente per quella dipendenza
- aggiornare requirements.txt con 'pip freeze > requirements.txt'



## Come visualizzare i file di log

Esistono due file che registrano l'attività di aggiornamento automatico del cron:
- *src/backend/logs_db_update.txt*: per informazioni consuntive sugli aggiornamenti terminati
- */var/log/cron.log*: per informazioni di monitoraggio delle attività del cron, cioè vengono registrati i log lanciati dallo script che esegue l'aggiornamento automatico

### Come visualizzare i file di log

#### Visualizzazione del file `logs_db_update.txt`
È possibile visualizzare il contenuto del file `logs_db_update.txt` seguendo i passaggi riportati di seguito:
1. Eseguire l'applicativo BuddyBot mediante Docker, come descritto nella sezione **Installazione** qui sopra.
2. Tramite Docker Desktop, accedere al container denominato `buddybot-backend`.
3. Recarsi nella sezione **Exec** del container.
4. Eseguire il comando:
  ```
  cat logs_db_update.txt
  ```
5. Se il container è stato appena creato, inizialmente il file sarà vuoto. Attendere qualche minuto e riprovare.

#### Visualizzazione del file `cron.log`
È possibile visualizzare il contenuto del file `cron.log` seguendo i passaggi riportati di seguito:
1. Eseguire l'applicativo BuddyBot mediante Docker, come descritto nella sezione **Installazione** qui sopra.
2. Tramite Docker Desktop, accedere al container denominato `buddybot-backend`.
3. Recarsi nella sezione **Exec** del container.
4. Eseguire il comando:
  ```
  cat /var/log/cron.log
  ```
5. Se il container è stato appena creato, inizialmente il file non esisterà. Attendere qualche minuto e riprovare. Poiché il file viene scritto progressivamente durante l'esecuzione del cron, è possibile visualizzare un'istantanea di quanto scritto fino al momento in cui si preme Invio. Riprovando ad eseguire `cat` dopo qualche minuto, si potrà visualizzare la segnalazione di fine aggiornamento.

Per entrambi i file, se si vuole accedere al terminale del container `buddybot-backend` senza usare l'interfaccia grafica ed il limitato terminale di Docker Desktop, è possibile utilizzare il terminale del proprio sistema operativo digitandovi:
  ```
  docker exec -it buddybot-backend /bin/bash
  ```
Diventa a questo punto possibile visualizzare i due file log con gli stessi comandi `cat` descritti sopra.
