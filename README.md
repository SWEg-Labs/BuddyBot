È necessario avere Docker installato

Per evitare possibili problemi di transizione da un sistema operativo MS-DOS (windows) della macchina a sistema operativo Unix del container è consigliato prima di tutto spostarsi sulla directory del file crontab ed eseguire "dos2unix crontab".

Per avviare il container eseguire il comando "docker compose up".
Docker se necessario costruirà le immagini di chroma e dell'applicazione python.

Per eseguire l'applicazione andare nel terminale del container (tra i Containers di Docker Desktop, selezionare "backend" e andare alla voce "Exec"), navigare alla directory dove c'è il file main.py ed eseguire "python main.py".
In alternativa dal terminale della macchina si può fare "docker exec -it buddybot-backend /bin/bash" per accedere al terminale del container chiamato buddybot-backend.

Se attendete 5 minuti dall'avvio del container, poi avviate l'applicazione ed inserite il comando "v" per vedere i documenti presenti nel database vedrete che il database non è vuoto.

Dopo aver fatto modifiche al codice eseguire "docker compose up --build" per far ricostruire le immagini con il codice aggiornato, altrimenti docker usa il codice vecchio per avviare i container.
