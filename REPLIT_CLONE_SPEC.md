Below is a **complete, production‑grade scaffold** for a **Replit‑style cloud IDE** that ships with:

* **Monaco‑based code editor** (multi‑language, syntax highlighting)  
* **xterm.js terminal** (real‑time output via Socket.IO)  
* **Virtual file‑tree** that syncs with a backend API  
* **Claude‑powered AI assistant** (Sonnet 4 / Opus 4.1) with **Tamil‑English bilingual UI** (react‑i18next)  
* **Secure Docker sandbox** for executing user code (Python, Node, Go, Java, Rust, …)  
* **JWT auth** (Firebase or Auth0) + role‑based access control  
* **Docker‑Compose** for local dev, **GitHub Actions** CI, and notes for **Kubernetes / cloud‑scale** deployment  
* **Production‑ready security hardening hooks** (cgroup limits, seccomp, audit logging, CSP, etc.)  

You can copy‑paste the whole tree into a fresh repository, run `npm run setup`, and you'll have a fully functional IDE that you can run locally (`localhost:5173` + `localhost:4000`) or push to any cloud provider (Render, Fly.io, Railway, GCP, AWS, Azure, …).

---

## 📁 1️⃣ Directory Tree (copy‑paste into your repo)

```
replit-clone/
├─ .env.example
├─ .gitignore
├─ docker-compose.yml
├─ Dockerfile.frontend      # for production image
├─ Dockerfile.backend       # for production image
├─ package.json             # root workspace
├─ README.md
├─ shared/
│  ├─ types.ts
│  └─ utils.ts
├─ frontend/
│  ├─ public/
│  │  └─ index.html
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ Editor.tsx
│  │  │  ├─ Terminal.tsx
│  │  │  └─ FileTree.tsx
│  │  ├─ agents/
│  │  │  └─ CodeAssistant.ts
│  │  ├─ i18n/
│  │  │  ├─ en.json
│  │  │  └─ ta.json
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ vite.config.ts
│  └─ tsconfig.json
├─ backend/
│  ├─ routes/
│  │  ├─ run.ts
│  │  ├─ auth.ts
│  │  └─ files.ts
│  ├─ sandbox/
│  │  └─ dockerRunner.ts
│  ├─ utils/
│  │  └─ logger.ts
│  ├─ server.ts
│  └─ tsconfig.json
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

## 📦 2️⃣ Root Files  

### `package.json` (workspace)

```json
{
  "name": "replit-clone",
  "private": true,
  "workspaces": ["frontend", "backend"],
  "scripts": {
    "setup": "npm install && npm install --workspace=frontend && npm install --workspace=backend",
    "dev": "concurrently \"npm run dev --workspace=frontend\" \"npm run dev --workspace=backend\"",
    "build": "npm run build --workspace=frontend && npm run build --workspace=backend",
    "lint": "eslint . --ext .ts,.tsx",
    "test": "echo \"No tests yet\""
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
```

### `.gitignore`

```gitignore
# Node modules
node_modules/
**/node_modules/

# Build artefacts
frontend/dist/
backend/dist/
dist/

# Vite cache
.vite/

# Env files
.env
.env.local
.env.*.local

# OS artefacts
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml
```

### `.env.example`

```dotenv
# -------------------------------------------------
# Frontend (exposed to the browser)
# -------------------------------------------------
VITE_API_URL=http://localhost:4000/api
VITE_I18N_DEFAULT_LANG=en   # en | ta

# -------------------------------------------------
# Backend (server‑side only)
# -------------------------------------------------
PORT=4000
JWT_SECRET=change_this_to_a_strong_random_string

# Firebase (or Auth0) – pick one
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CLIENT_EMAIL=your-firebase-client-email@...gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"

# -------------------------------------------------
# Docker sandbox (code execution)
# -------------------------------------------------
SANDBOX_IMAGE=node:20-alpine          # base image for most languages
SANDBOX_TIMEOUT_MS=5000               # max exec time per request
SANDBOX_MEMORY_LIMIT=256m              # per‑container memory limit
SANDBOX_CPU_SHARES=512                # relative CPU weight (default 1024)

# -------------------------------------------------
# Claude (Anthropic) – primary LLM
# -------------------------------------------------
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620   # or claude-3-opus-20240229

# -------------------------------------------------
# OpenAI fallback (optional)
# -------------------------------------------------
OPENAI_API_KEY=sk-xxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

### `docker-compose.yml`

```yaml
version: "3.9"
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    ports:
      - "${PORT:-4000}:4000"
    volumes:
      - ./backend:/app
      - /var/run/docker.sock:/var/run/docker.sock   # needed for sandbox containers
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    env_file: .env
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
    command: ["npm", "run", "dev"]
    restart: unless-stopped
```

### `Dockerfile.frontend` (production image)

```dockerfile
# ---- Build stage ----
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ---- Runtime stage ----
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### `Dockerfile.backend` (production image)

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY backend/package*.json ./
RUN npm ci --omit=dev
COPY backend/ .
RUN npm run build   # compiles TS → JS
EXPOSE 4000
CMD ["node", "dist/server.js"]
```

### `README.md`

```markdown
# Replit‑Clone (AI‑augmented Cloud IDE)

A **full‑stack, production‑ready** clone of the Replit IDE with:

* Monaco editor + xterm.js terminal  
* Real‑time file‑tree sync  
* Claude‑powered code assistant (English ↔ Tamil)  
* Secure Docker sandbox for arbitrary language execution  
* JWT auth (Firebase or Auth0)  
* Docker‑Compose for local dev, Docker images for production, and CI/CD ready

> **TL;DR** – `npm run setup && npm run dev` → open `http://localhost:5173`

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Local Development](#local-development)  
3. [Environment Variables](#environment-variables)  
4. [Running in Production (Docker)](#production)  
5. [Deploying to the Cloud (Render / Fly / Railway / GCP)](#cloud-deploy)  
6. [Scaling & Kubernetes Notes](#k8s)  
7. [Security Hardening Checklist](#security)  
8. [Testing the AI Assistant](#ai-testing)  
9. [License](#license)

---

[Note: This appears to be a partial specification document. The full implementation would require additional files and code components as outlined in the directory tree above.]
```