# FastAPI + Railway Deployment Tutorial (Automotive Repair Shop Scheduler)

This repository demonstrates how to build and deploy a **FastAPI** service for an automotive repair shop scheduling problem using **Google OR-Tools**.

The tutorial goal is simple: help learners deploy a real FastAPI backend on **Railway** and connect it to a frontend.

## Live End-to-End Example

If you want to see a complete deployed setup (**frontend + backend**) in production, visit:

- https://milp.netlify.app/

## What This API Does

The API receives a scheduling payload and returns optimization results:

- A Gantt chart figure (as Plotly JSON)
- Per-station statistics (overtime, idle time, station cost)
- Optional warning when the solution is near-optimal due to server limits
- Error message when no feasible schedule exists

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- OR-Tools
- Plotly
- Docker (for container deployment)
- Railway (hosting)

## Project Structure

```text
.
|- app/
|  |- main.py               # FastAPI app and routes
|  |- optimiser.py          # Runs optimization workflow
|  |- OPT/
|     |- Idle_Overtime.py   # Core optimization model logic
|     |- gantt_plotter.py   # Gantt chart generation
|- requirements.txt
|- Dockerfile
|- docker-compose.yml
|- schedule.json            # Sample request payload
|- schedule2.json           # Alternative sample payload
```

## API Endpoints

### `GET /`
Health route.

**Response example**

```json
{ "msg": "Up & running - hit /docs for Swagger UI" }
```

### `POST /solve`
Runs the scheduler with your payload.

**Request body (schema overview)**

- `T`: overtime cost per station
- `I`: idle-time cost per station
- `ST`: shift length per station (minutes)
- `OV_limit`: max overtime per station (minutes, optional)
- `d`: duration matrix (`car -> repair type -> minutes`)
- `e`: eligibility matrix (`repair type -> station -> 0/1`)

**Success response shape**

```json
{
  "figure": "{...plotly-json...}",
  "stats": {
    "1": [120, 40, 44.0],
    "2": [90, 55, 38.5]
  }
}
```

**Near-optimal response shape**

```json
{
  "figure": "{...plotly-json...}",
  "stats": { "1": [120, 40, 44.0] },
  "warning": "Returned solution is (near)-optimal due to limited server time..."
}
```

**Infeasible response shape**

```json
{
  "error": "No feasible solution found for the given data..."
}
```

## Run Locally (No Docker)

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Start the API

```bash
uvicorn app.main:app --reload
```

### 4) Open docs

- Swagger UI: http://127.0.0.1:8000/docs
- Health route: http://127.0.0.1:8000/

## Test the `/solve` Endpoint

Use the provided sample payload:

```bash
curl -X POST "http://127.0.0.1:8000/solve" \
  -H "Content-Type: application/json" \
  --data @schedule.json
```

PowerShell alternative:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/solve" \
  -Method Post \
  -ContentType "application/json" \
  -Body (Get-Content .\schedule.json -Raw)
```

## Run with Docker

### Build image

```bash
docker build -t optimiser-api .
```

### Run container

```bash
docker run --rm -p 8000:8000 optimiser-api
```

## Deploy to Railway (Step-by-Step Tutorial)

### Option A: Deploy with Dockerfile (recommended)

1. Push your project to GitHub.
2. In Railway, click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. If this API is in a subfolder (monorepo), set the Railway **Root Directory** to that folder.
5. Railway detects `Dockerfile` and builds automatically.
6. Deploy and open your generated Railway domain.
7. Verify:
   - `GET /`
   - `GET /docs`
   - `POST /solve`

### Option B: Deploy without Dockerfile (Nixpacks)

If you prefer buildpacks instead of Docker, set:

- Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway injects `$PORT` automatically.

## Connect Frontend to Railway API

Set your frontend API URL to:

```text
https://<your-railway-domain>/solve
```

For Next.js frontend, use:

```env
NEXT_PUBLIC_API_URL=https://<your-railway-domain>/solve
```

## CORS Configuration

If your frontend domain changes, update `allow_origins` in `app/main.py`.

Typical local + production origins to allow:

- `http://localhost:3000`
- Your Netlify/Vercel domain
- Any custom domain you use

## Common Issues and Fixes

### 1) `ModuleNotFoundError` at startup

- Make sure you run commands from the project root.
- Ensure dependencies are installed from `requirements.txt`.

### 2) CORS errors in browser

- Add your frontend domain to `allow_origins` in `app/main.py`.
- Redeploy after changing CORS.

### 3) Timeout or slow solve on free tier

- Reduce input size (fewer cars/repairs).
- Increase station shift time or eligibility coverage.
- Use paid compute for larger instances.

### 4) Railway deploy fails due wrong root folder

- Set the correct **Root Directory** in Railway project settings.

## Tutorial Teaching Flow (Suggested)

If you are using this repo in a workshop/class:

1. Explain payload structure (`T`, `I`, `ST`, `d`, `e`, `OV_limit`).
2. Run locally and test via `/docs`.
3. Validate with `schedule.json`.
4. Deploy to Railway.
5. Connect frontend with `NEXT_PUBLIC_API_URL`.
6. Compare local and deployed outputs.

## License and Citation

If you use this model in research, cite the associated work in your publication and include a link to the live demo:

- https://milp.netlify.app/
