# Insight Inbox - Project Wiki

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Frontend (Next.js)](#frontend-nextjs)
  - [App Router & Pages](#app-router--pages)
  - [Layout & Theming](#layout--theming)
  - [API Client Library](#api-client-library)
  - [Styling with Tailwind CSS](#styling-with-tailwind-css)
- [Backend (FastAPI)](#backend-fastapi)
  - [Application Entry Point](#application-entry-point)
  - [Routers](#routers)
  - [Data Models](#data-models)
  - [CORS Configuration](#cors-configuration)
  - [Core Configuration](#core-configuration)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
- [API Reference](#api-reference)
- [Scripts & Commands](#scripts--commands)
- [Configuration Files](#configuration-files)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Project Overview

**Insight Inbox** is a full-stack web application built with a **Next.js 16** frontend and a **Python FastAPI** backend. The application provides a note-taking system where users can create and list notes. The project is structured as a monorepo containing both the frontend and backend codebases, making it easy to develop and manage both layers together.

The project name in `package.json` is `insight-inbox-web`, and the API is titled **Insight Inbox API** (v0.1.0).

---

## Architecture

The application follows a **decoupled client-server architecture**:

```
+-------------------+         HTTP (REST)         +-------------------+
|                   |  ----------------------->   |                   |
|   Next.js 16      |                             |   FastAPI 0.135   |
|   (React 19)      |  <-----------------------   |   (Python)        |
|   Port: 3000      |         JSON Responses      |   Port: 8000      |
|                   |                             |                   |
+-------------------+                             +-------------------+
     Frontend                                          Backend
```

- **Frontend** serves the UI on `http://localhost:3000`
- **Backend** API runs on `http://localhost:8000`
- Communication is via RESTful JSON API calls
- CORS middleware on the backend allows cross-origin requests from the frontend

---

## Tech Stack

### Frontend

| Technology       | Version   | Purpose                                    |
|------------------|-----------|--------------------------------------------|
| Next.js          | 16.1.6    | React framework with App Router            |
| React            | 19.2.3    | UI component library                       |
| React DOM        | 19.2.3    | React rendering for the browser            |
| TypeScript       | ^5        | Type-safe JavaScript                       |
| Tailwind CSS     | ^4        | Utility-first CSS framework                |
| ESLint           | ^9        | Code linting                               |
| pnpm             | -         | Package manager                            |

### Backend

| Technology       | Version   | Purpose                                    |
|------------------|-----------|--------------------------------------------|
| FastAPI          | 0.135.1   | High-performance Python web framework      |
| Uvicorn          | 0.41.0    | ASGI server for FastAPI                    |
| Pydantic         | 2.12.5    | Data validation and serialization          |
| Starlette        | 0.52.1    | ASGI toolkit (FastAPI dependency)          |
| python-dotenv    | 1.2.2     | Environment variable management            |
| PyYAML           | 6.0.3     | YAML file parsing                          |
| websockets       | 16.0      | WebSocket protocol support                 |

---

## Directory Structure

```
nodejs_hands_on/
|
|-- app/                        # Next.js App Router directory (frontend pages)
|   |-- favicon.ico             # Browser tab icon
|   |-- globals.css             # Global CSS styles (Tailwind + CSS variables)
|   |-- layout.tsx              # Root layout component (HTML shell, fonts)
|   |-- page.tsx                # Home page component (note creation UI)
|
|-- api/                        # Python FastAPI backend
|   |-- requirements.txt        # Python dependencies
|   |-- app/                    # FastAPI application package
|       |-- main.py             # FastAPI app initialization, middleware, routers
|       |-- core/               # Core configuration module
|       |   |-- config.py       # Application configuration (placeholder)
|       |-- routers/            # API route handlers
|           |-- health.py       # Health check endpoint
|           |-- notes.py        # Notes CRUD endpoints
|
|-- lib/                        # Shared frontend utilities
|   |-- api.ts                  # API client for backend communication
|
|-- public/                     # Static assets served by Next.js
|   |-- file.svg
|   |-- globe.svg
|   |-- next.svg
|   |-- vercel.svg
|   |-- window.svg
|
|-- eslint.config.mjs           # ESLint configuration (Next.js + TypeScript)
|-- next.config.ts              # Next.js configuration
|-- package.json                # Node.js dependencies and scripts
|-- pnpm-lock.yaml              # pnpm dependency lock file
|-- pnpm-workspace.yaml         # pnpm workspace configuration
|-- postcss.config.mjs          # PostCSS configuration (Tailwind plugin)
|-- tsconfig.json               # TypeScript compiler configuration
|-- .gitignore                  # Git ignore rules
|-- README.md                   # Basic project readme
```

---

## Frontend (Next.js)

### App Router & Pages

The frontend uses the **Next.js App Router** (the `app/` directory convention). Currently, there is one page:

#### Home Page (`app/page.tsx`)

- Marked as a **client component** (`"use client"`) to enable React hooks and interactivity
- Renders the main **"Insight Inbox"** heading
- Provides a **"Create test note"** button that:
  1. Calls the `createNote()` API function with hardcoded test data (`title: "Test"`, `content: "From Next.js"`)
  2. Displays a status message showing the created note's ID on success
  3. Shows an error message on failure
- Uses React's `useState` hook for managing the status message

```tsx
// Simplified flow
const [msg, setMsg] = useState<string>("");

async function onCreate() {
  setMsg("Creating...");
  const note = await createNote({ title: "Test", content: "From Next.js" });
  setMsg(`Created note: ${note.id}`);
}
```

### Layout & Theming

#### Root Layout (`app/layout.tsx`)

- Defines the HTML document structure (`<html>`, `<body>`)
- Loads **Geist** font family (Sans and Mono variants) via `next/font/google`
- Applies font CSS variables (`--font-geist-sans`, `--font-geist-mono`) to the body
- Enables `antialiased` text rendering via Tailwind
- Sets page metadata:
  - **Title**: "Create Next App"
  - **Description**: "Generated by create next app"

#### Global Styles (`app/globals.css`)

- Imports Tailwind CSS (`@import "tailwindcss"`)
- Defines CSS custom properties for theming:
  - `--background`: `#ffffff` (light) / `#0a0a0a` (dark)
  - `--foreground`: `#171717` (light) / `#ededed` (dark)
- Uses `@media (prefers-color-scheme: dark)` for automatic dark mode support
- Maps CSS variables to Tailwind theme tokens via `@theme inline`
- Sets body font to `Arial, Helvetica, sans-serif`

### API Client Library

#### `lib/api.ts`

This module provides a typed API client for communicating with the FastAPI backend:

- **Base URL Configuration**:
  - Uses `NEXT_PUBLIC_API_BASE_URL` environment variable if set
  - Falls back to `http://localhost:8000` for local development

- **`createNote(input)`** - Creates a new note
  - **Method**: `POST`
  - **Endpoint**: `{API_BASE}/notes`
  - **Headers**: `Content-Type: application/json`
  - **Body**: `{ title: string, content: string }`
  - **Returns**: The created note object (parsed JSON)
  - **Error Handling**: Throws an `Error` with the HTTP status code on non-OK responses

### Styling with Tailwind CSS

The project uses **Tailwind CSS v4** with the following setup:

- **PostCSS Plugin**: Configured via `postcss.config.mjs` using `@tailwindcss/postcss`
- **Theme Integration**: Custom CSS variables are mapped to Tailwind tokens in `globals.css`
- **Usage**: Utility classes are used directly in JSX components (e.g., `min-h-screen`, `p-8`, `text-2xl`, `font-bold`, `rounded`, `bg-black`, etc.)

---

## Backend (FastAPI)

### Application Entry Point

#### `api/app/main.py`

The FastAPI application is initialized here:

```python
app = FastAPI(title="Insight Inbox API", version="0.1.0")
```

- Creates the FastAPI app instance with title and version metadata
- Configures CORS middleware for frontend communication
- Registers route handlers (health and notes routers)

### Routers

The API uses FastAPI's `APIRouter` for modular route organization:

#### Health Router (`api/app/routers/health.py`)

| Method | Endpoint   | Description            | Response                |
|--------|-----------|------------------------|-------------------------|
| GET    | `/health` | Health check endpoint  | `{"status": "ok"}`     |

Simple health check endpoint to verify the API is running.

#### Notes Router (`api/app/routers/notes.py`)

All notes endpoints are prefixed with `/notes` and tagged as `"notes"`.

| Method | Endpoint  | Description          | Request Body                        | Response                                          |
|--------|----------|----------------------|-------------------------------------|---------------------------------------------------|
| POST   | `/notes` | Create a new note    | `{"title": "str", "content": "str"}` | `{"id": "uuid", "title": "str", "content": "str"}` |
| GET    | `/notes` | List all notes       | -                                   | `{"items": [], "next_cursor": null}`              |

> **Note**: Both endpoints currently return **mock responses**. The `create_note` endpoint generates a random UUID for each new note. The `list_notes` endpoint returns an empty list. Database integration is planned for the future.

### Data Models

#### `NoteCreate` (Pydantic Model)

```python
class NoteCreate(BaseModel):
    title: str
    content: str
```

Used for validating the request body when creating a note. Pydantic automatically handles:
- Type validation
- JSON serialization/deserialization
- OpenAPI schema generation

### CORS Configuration

The backend is configured to allow cross-origin requests from the Next.js frontend:

```python
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- Currently allows requests from `localhost:3000` (both HTTP and HTTPS)
- All HTTP methods and headers are permitted
- Credentials (cookies, auth headers) are allowed
- A comment notes that this will be switched to environment-based configuration later

### Core Configuration

The `api/app/core/config.py` file is currently a **placeholder** (empty file) reserved for future application configuration such as database connection strings, API keys, and other settings.

---

## Environment Variables

| Variable                      | Layer    | Required | Default                  | Description                                    |
|-------------------------------|----------|----------|--------------------------|------------------------------------------------|
| `NEXT_PUBLIC_API_BASE_URL`    | Frontend | No       | `http://localhost:8000`  | Base URL for the FastAPI backend               |

Additional environment variables can be configured through the `python-dotenv` package on the backend side. The `.gitignore` excludes all `.env*` files from version control.

---

## Getting Started

### Prerequisites

- **Node.js** (v18+ recommended)
- **pnpm** (package manager for the frontend)
- **Python 3.10+** (for the backend)
- **pip** or **venv** (for Python dependency management)

### Frontend Setup

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Start the development server**:
   ```bash
   pnpm dev
   ```

3. **Open in browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Backend Setup

1. **Create a virtual environment**:
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **API documentation**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### `GET /health`

Returns the health status of the API.

**Response** (`200 OK`):
```json
{
  "status": "ok"
}
```

#### `POST /notes`

Creates a new note (currently returns mock data).

**Request Body**:
```json
{
  "title": "My Note Title",
  "content": "The content of the note."
}
```

**Response** (`200 OK`):
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "My Note Title",
  "content": "The content of the note."
}
```

#### `GET /notes`

Lists all notes (currently returns an empty mock list).

**Response** (`200 OK`):
```json
{
  "items": [],
  "next_cursor": null
}
```

---

## Scripts & Commands

### Frontend (pnpm)

| Command         | Description                              |
|-----------------|------------------------------------------|
| `pnpm dev`      | Start Next.js development server         |
| `pnpm build`    | Create an optimized production build     |
| `pnpm start`    | Start the production server              |
| `pnpm lint`     | Run ESLint on the codebase               |

### Backend (Python)

| Command                                        | Description                              |
|------------------------------------------------|------------------------------------------|
| `uvicorn app.main:app --reload --port 8000`    | Start FastAPI with hot reload            |
| `pip install -r requirements.txt`              | Install Python dependencies              |

---

## Configuration Files

### `next.config.ts`

Currently uses the default Next.js configuration with no custom options. This is where you would add:
- Image optimization settings
- Rewrites/redirects
- Webpack customization
- Environment variable exposure

### `tsconfig.json`

Key TypeScript settings:
- **Target**: ES2017
- **Module**: ESNext with bundler resolution
- **Strict mode**: Enabled
- **JSX**: react-jsx (automatic runtime)
- **Path aliases**: `@/*` maps to the project root (`"./*"`)
- **Incremental compilation**: Enabled for faster rebuilds
- **Next.js plugin**: Included for enhanced type checking

### `eslint.config.mjs`

Uses the flat config format (ESLint v9+):
- Extends `eslint-config-next/core-web-vitals` for React and Next.js best practices
- Extends `eslint-config-next/typescript` for TypeScript-specific rules
- Ignores build output directories (`.next/`, `out/`, `build/`)

### `postcss.config.mjs`

Configures PostCSS with the `@tailwindcss/postcss` plugin for Tailwind CSS v4 processing.

### `pnpm-workspace.yaml`

Configures pnpm workspace settings:
- Ignores built dependencies for `sharp` and `unrs-resolver` (build optimization)

### `.gitignore`

Ignores:
- `node_modules/` - Node.js dependencies
- `.next/`, `out/`, `build/` - Next.js build output
- `.env*` - Environment variable files
- `.vercel/` - Vercel deployment config
- `*.tsbuildinfo`, `next-env.d.ts` - TypeScript build artifacts
- `api/venv/` - Python virtual environment
- `*.pem` - SSL certificates
- Debug logs from npm, yarn, pnpm

---

## Deployment

### Frontend (Vercel)

The project is set up for deployment on **Vercel**:
1. Connect the GitHub repository to Vercel
2. Set the `NEXT_PUBLIC_API_BASE_URL` environment variable to point to the deployed backend URL
3. Vercel will automatically build and deploy on each push

### Backend

The FastAPI backend can be deployed to any platform that supports Python ASGI applications:
- **Fly.io**
- **Railway**
- **AWS Lambda** (with Mangum adapter)
- **Google Cloud Run**
- **Docker** container on any cloud provider

Remember to update the CORS `origins` list in `api/app/main.py` to include the production frontend URL.

---

## Contributing

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes** and commit with descriptive messages
4. **Run linting**: `pnpm lint`
5. **Push** to your branch: `git push origin feature/my-feature`
6. **Open a Pull Request** against `main`

### Code Style

- **Frontend**: Follow ESLint rules (Next.js Core Web Vitals + TypeScript)
- **Backend**: Follow PEP 8 Python style guidelines
- **CSS**: Use Tailwind utility classes; avoid custom CSS when possible
- **TypeScript**: Enable strict mode; avoid `any` types
