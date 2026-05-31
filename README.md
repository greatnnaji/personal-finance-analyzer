[![CI](https://github.com/greatnnaji/personal-finance-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/greatnnaji/personal-finance-analyzer/actions/workflows/ci.yml)
# Personal Finance Analyzer
Full-stack app for uploading transaction files, categorizing spending, and viewing analysis in a React dashboard.

## Requirements

- Python 3.11
- Conda
- Node.js 20+ and npm

## Quick Start

Clone the repo and install the backend environment:

```bash
git clone https://github.com/greatnnaji/personal-finance-analyzer.git
cd personal-finance-analyzer
conda env update --file environment.yml --prune
conda activate personalFinanceAnalyzer
```

## Run the Backend

Start the Flask API from the `backend` folder:

```bash
cd backend
python app.py
```

The API runs on `http://localhost:5050`.

For production-style deployment, use Gunicorn:

```bash
cd backend
gunicorn -b 0.0.0.0:5050 wsgi:application
```

Backend runtime settings live in `backend/.env.example`.

## Run the Frontend

Start the React app from the `frontend` folder:

```bash
cd frontend
npm install
npm start
```

The UI runs on `http://localhost:3000`.

Frontend API configuration lives in `frontend/.env.example`.

## Tests

Backend:

```bash
cd backend
python -m pytest -v
```

Frontend:

```bash
cd frontend
npm test
```

## Supported File Types

- CSV
- Excel (`.xlsx`, `.xls`)
- PDF

## Workflow

1. Start the backend in one terminal.
2. Start the frontend in a second terminal.
3. Open `http://localhost:3000`.
4. Upload a CSV, Excel, or PDF transaction file.
5. Review the analysis results and charts.

## Notes

- `environment.yml` is the source of truth for backend dependencies.
- `backend/.env.example` and `frontend/.env.example` document the expected local env values.
- `npm test` runs in CI mode, so it exits after the suite finishes.
