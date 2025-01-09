# README

## Prerequisiti
- È necessario avere Docker installato

## Avvio del container
Per avviare il container eseguire il comando:
```
docker compose up --build
```

## Esecuzione dell'applicazione
- Andare nel terminale del container
  - Tra i Containers di Docker Desktop, selezionare "backend"
  - Entrati nel container andare alla voce "Exec"
- Navigare alla directory dove c'è il file main.py ed eseguire:
  ```
  python main.py
  ```
- Se attendete 5 minuti dall'avvio del container ed inserite nel chatBot il comando "v" per vedere i documenti presenti nel database vedrete che il database non è vuoto.

## .env
Tutte le variabili di sistema di configurazione sono nel dockerfile. Nel .env servono solo le sequenti voci:
```
OPENAI_API_KEY = la_tua_chiave_openai
OPENAI_MODEL_NAME = modello_llm_scelto
OPENAI_EMBEDDING_MODEL_NAME = embedding_model_scelto
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
