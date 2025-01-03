# BuddyBot
Repository contenente il codice sorgente di BuddyBot, capitolato C9 di Ingegneria del Software 2024/25, proposto dal proponente AzzurroDigitale.

Per eseguire BuddyBot, occorre innanzitutto configurare il database vettoriale Chroma.


## Chroma

### La prima volta

Scaricare l'immagine Docker di ChromaDB:
```
docker pull chromadb/chroma
```

Runnare l'immagine Docker creando un container, e quindi attivare il database vettoriale
```
docker run -p 8000:8000 chromadb/chroma
```

Adesso il database vettoriale è caricato in:
```
http://localhost:8000/
```

Ora, per capire qual è l'id del container, aprire un altro terminale ed eseguire il comando per visualizzare i container attivi correntemente:
```
docker ps
```
E segnarsi l'id del container da qualche parte. Ad esempio, il mio container è 65ccf1331c92

A questo punto, per chiudere il database vettoriale basterà eseguire:
```
docker stop 65ccf1331c92
```
Sostituendo ovviamente l'id del container con quello personale


### Dalla seconda volta in poi

E poi per riaprirlo:
```
docker start 65ccf1331c92
```
Qui la schermata sarà diversa dalla prima run, poichè infatti il processo non rimarrà attivo sul terminale, ma bensì continuerà in background

Poi lo si può richiudere:
```
docker stop 65ccf1331c92
```

E così via, il proprio container lo si può chiudere e riaprire a piacimento.

Se dopo averlo chiuso non ci si ricorda più l'id del container, è possibile trovarlo eseguendo il comando per visualizzare i container totali presenti nella macchina:
```
docker ps -a
```
E cercare il Container ID corrispondente all'image "chromadb/chroma".



Successivamente, una volta che il database vettoriale Chroma è attivo, è possibile procedere nel far eseguire l'app:

## Esecuzione del backend in un Python virtual enviroment

### La prima volta

Occorre preparare il virtual enviroment:

```shell
python -m venv venv
```

Verrà adesso generata una cartella locale chiamata "venv", listata nel .gitignore e quindi non versionata da Git.
Poi, occorre attivare l'ambiente:

In Windows:
```shell
. src/backend/venv/scripts/activate
```
In Linux:
```shell
source src/backend/venv/bin/activate
```

Installare le dipendenze:

```shell
pip install -r src/backend/requirements.txt
```

E infine eseguire il backend dell'app:

```shell
python src/backend/main.py
```

Poi poni la domanda, ricevi la risposta, e concludi la conversazione digitando "exit".

Per chiudere l'ambiente virtuale:

```shell
deactivate
```

### Dalla seconda volta in poi

Attivare l'ambiente virtuale:

In Windows:
```shell
. src/backend/venv/scripts/activate
```
In Linux:
```shell
source src/backend/venv/bin/activate
```

Runnare il backend dell'app

```shell
python src/backend/main.py
```

Utilizzare l'app.  
Chiudere l'app digitando "exit".

Infine, chiudere l'ambiente virtuale

```shell
deactivate
```