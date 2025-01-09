È necessario avere Docker installato

Per avviare il container eseguire il comando "docker compose up --build".
Per eseguire l'applicazione andare nel terminale del container (tra i Containers di Docker Desktop, selezionare "backend" e andare alla voce "Exec"), navigare alla directory dove c'è il file main.py ed eseguire "python main.py".
Se attendete 5 minuti dall'avvio del container, poi avviate l'applicazione ed inserite il comando "v" per vedere i documenti presenti nel database vedrete che il database non è vuoto.

Tutte le variabili di sistema di configurazione sono nel dockerfile. Nel .env servono solo url verso servizi esterni e chiavi/codici vari.
