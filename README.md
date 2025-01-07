È necessario avere Docker installato

Per evitare possibili problemi di transizione da un sistema operativo MS-DOS (windows) della macchina a sistema operativo Unix del container è consigliato prima di tutto spostarsi sulla directory del file crontab ed eseguire "dos2unix".

Per avviare il container eseguire il comando "docker compose up".
Docker se necessario costruirà le immagini di chroma e dell'applicazione python.
Per eseguire l'applicazione andare nel terminale del container (tra i Containers di Docker Desktop, selezionare "backend" e andare alla voce "Exec"), navigare alla directory dove c'è il file main.py ed eseguire "python main.py".
Se attendete 5 minuti dall'avvio del container, poi avviate l'applicazione ed inserite il comando "v" per vedere i documenti presenti nel database vedrete che il database non è vuoto.