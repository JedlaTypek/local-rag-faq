# Návod na spuštění projektu "Easy Local RAG API"

Tento projekt běží v Docker kontejnerech (aplikace a vektorová databáze Qdrant), ale spoléhá se na to, že **Ollama** běží lokálně přímo na vašem hostitelském počítači (mimo Docker).

## Prerekvizity

1. **Nainstalovaný Docker a Docker Compose** 
   - Používá se pro spuštění aplikace a vektorové databáze Qdrant.
2. **Nainstalovaná Ollama**
   - Stáhněte a nainstalujte z [ollama.com](https://ollama.com/).
   - Ollama musí běžet na vašem hostitelském počítači (standardně na portu `11434`).
3. **Stažený model v Ollamě**
   - Aplikace v základu očekává model `llama3` (nebo jiný, který máte specifikovaný v souboru `.env`).
   - Pro jeho stažení spusťte v terminálu (mimo Docker):
     ```bash
     ollama pull llama3
     ollama pull mxbai-embed-large
     ```

## Nastavení prostředí (.env)

V kořenové složce projektu se nachází soubor `.env`, který obsahuje základní konfiguraci:
```env
QDRANT_HOST=qdrant
QDRANT_PORT=6333
OLLAMA_BASE_URL=http://host.docker.internal:11434/
OLLAMA_MODEL=llama3
OLLAMA_EMBEDDING_MODEL=mxbai-embed-large
```

Klíčové je zde nastavení `OLLAMA_BASE_URL`. Použitím `host.docker.internal` říkáme Docker kontejneru s naší aplikací, aby se připojil na port 11434 hostitelského počítače, kde běží vaše lokální Ollama. *(V `docker-compose.yaml` je explicitně povoleno mapování host-gateway, takže to bude na Linuxu bez problémů fungovat).*

## Spuštění celého projektu

Veškeré spouštění obstará Docker Compose. V kořenové složce projektu (tam, kde je soubor `docker-compose.yaml`) spusťte následující příkaz:

```bash
docker compose up -d --build
```

Co se stane:
1. Stáhne se a spustí image pro **Qdrant** (vektorová databáze) na portech `6333` a `6334`. Data ukládá lokálně do složky `./qdrant_storage`.
2. Sestaví se a spustí kontejner s FastAPI **aplikací** (připojí vaši aktuální složku do kontejneru pro auto-reload).
3. Aplikace bude dostupná na vašem stroji na adrese **http://localhost:8000**.

## Ověření, že vše funguje

1. **Zkontrolujte kontejnery:**
   ```bash
   docker compose ps
   ```
2. **Vyzkoušejte API Root (v prohlížeči nebo curl):**
   - Otevřete: http://localhost:8000/
   - Měli byste dostat zprávu typu: `{"message": "Welcome to Easy Local RAG API"}`
3. **Zkontrolujte FastAPI Swagger UI (dokumentace API):**
   - Otevřete: http://localhost:8000/docs
   - Zde uvidíte endpointy pro Ingest a Ask (`/api/v1/...`).

## Zastavení aplikace

Jakmile budete chtít aplikaci ukončit, zavolejte ve stejné složce:

```bash
docker compose down
```
*(Pokud budete měnit kód sítě nebo závislosti, docker se musí při dalším spuštění přebuildovat pomocí `--build` argumentu.)*
