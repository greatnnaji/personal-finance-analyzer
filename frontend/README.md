# Frontend

React UI for the personal finance analyzer.

## Requirements

- Node.js 20+ and npm

## Setup

From the repo root:

```bash
cd frontend
npm install
```

## API Configuration

Copy `frontend/.env.example` to `frontend/.env.local` if you want to point the app at a backend other than `http://localhost:5050`.

Example:

```bash
REACT_APP_API_BASE_URL=http://localhost:5050
```

If `REACT_APP_API_BASE_URL` is not set, the app falls back to `http://localhost:5050`.

## Run

```bash
npm start
```

The app runs at `http://localhost:3000`.

## Build

```bash
npm run build
```

## Tests

```bash
npm test
```

The test script runs in CI mode and exits after the suite finishes.
