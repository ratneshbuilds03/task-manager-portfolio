# Task Manager Frontend

React 18 and Vite client for the Task Manager REST API.

## Setup

From this directory, install the locked dependencies and start the development server:

```powershell
npm ci
npm run dev
```

Vite runs at `http://localhost:3000` and proxies `/api` requests to `http://localhost:5000`. Set `VITE_API_URL` in a local Vite env file to override the API base URL; `.env.example` documents the default proxy path. Do not commit local env files.

## Build

```powershell
npm run build
npm audit --audit-level=moderate
```

The frontend uses React Router, Axios, and React Icons. Auth requests use the API's `access_token` response; protected task requests attach it as a Bearer token. Available task operations include create, list, read, update, delete, completion toggling, status/priority filters, and pagination.
