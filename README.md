[![CI](https://github.com/greatnnaji/personal-finance-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/greatnnaji/personal-finance-analyzer/actions/workflows/ci.yml)
# Personal Finance Analyzer
Full-stack app for uploading transaction files, categorizing spending, and viewing analysis in a React dashboard.

## Get Started
```bash
git clone https://github.com/greatnnaji/personal-finance-analyzer.git
cd personal-finance-analyzer
```
## Requirements

- Python 3.11
- Conda
- Node.js 20+ and npm

## Install

From the repo root:

```bash
conda env update --file environment.yml --prune
```

Then activate the environment:

```bash
conda activate personalFinanceAnalyzer
```

## Run the backend

Start the Flask API from the `backend` folder:

```bash
cd backend
conda activate personalFinanceAnalyzer
python app.py
```

The API runs on `http://localhost:5050`.

For production-style deployment, use a WSGI server such as Gunicorn:

```bash
cd backend
gunicorn -b 0.0.0.0:5050 wsgi:application
```

The backend reads runtime settings from environment variables or a local `.env` file. See `backend/.env.example` for the supported values.

## Run the frontend

Start the React app from the `frontend` folder:

```bash
cd frontend
npm install
npm start
```

The UI runs on `http://localhost:3000`.

## Run tests

Backend tests:

```bash
cd backend
conda activate personalFinanceAnalyzer
python -m pytest -v
```

Frontend tests:

```bash
cd frontend
npm test
```

## Typical workflow

1. Start the backend in one terminal.
2. Start the frontend in a second terminal.
3. Open `http://localhost:3000`.
4. Upload a CSV, Excel, or PDF transaction file.
5. Review the analysis results and charts.

## Supported file types

- CSV
- Excel (`.xlsx`, `.xls`)
- PDF

## Notes

- `environment.yml` is the source of truth for backend dependencies.
- The frontend test script runs in CI mode, so `npm test` exits after the suite finishes.
