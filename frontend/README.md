# GameHub — Frontend

React + TypeScript + Vite + Tailwind CSS frontend for the GameHub microservices platform.

## Stack

- React 19
- TypeScript
- Vite 8
- Tailwind CSS 4
- React Router 7

## Getting started

```bash
npm install
npm run dev
```

App runs at http://localhost:5173.

## Mock mode

The backend is not required to run the frontend. Use mock data with:

```bash
cd services/frontend
VITE_USE_MOCK=true npm run dev
```

When the backend is ready, just run without the flag:

```bash
npm run dev
```

The mock simulates a ~300ms network delay and supports search (case-insensitive title match). No code changes needed to switch — just the env var.

## Project structure

```
src/
├── api/
│   ├── client.ts        # base fetch wrapper → http://localhost:8000
│   ├── users.ts         # usersApi — list, get, create
│   ├── games.ts         # gamesApi — list, get, search, create
│   ├── mock.ts          # mock implementations (same interface)
│   └── mock-data.json   # sample users and games
├── pages/
│   ├── UsersPage.tsx    # /users
│   └── GamesPage.tsx    # /games
├── main.tsx             # app entry point, BrowserRouter
└── App.tsx              # route definitions
```

## API

All requests go through the gateway at `http://localhost:8000`.
From Module 3 onward, never call service ports directly.

| Page | Route | Backend |
|------|-------|---------|
| Users | `/users` | `GET /v1/users` |
| Games | `/games` | `GET /v1/games`, `GET /v1/games/search` |
