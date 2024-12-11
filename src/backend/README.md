# Per Chroma:


## La prima volta

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
E segnarsi l'id del container da qualche parte. Ad esempio, il mio su Linux è b4cf34dea51a, mentre su Windows è 65ccf1331c92

A questo punto, per chiudere il database vettoriale basterà eseguire:
```
docker stop 65ccf1331c92
```
Sostituendo ovviamente l'id del container con quello personale





## Dalla seconda in poi

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