# wolfinvest
Investing app without donate

Install dependencies
```bash
pip install -e .
```

Set env values
```bash
DB_URI=postgresql+asyncpg://user:password@localhost/database
AUTH_SECRET_KEY=secret_key
TICKERS_FILE_PATH=tickers.json
```

Run
```bash
uvicorn app.presentation.api:app
```
