# Autism Spectrum Multi-Agent Simulation & Bias Research Dashboard

A research platform studying implicit autism-related bias in LLMs through multi-agent
conversation simulation. Agents are assigned personas (non-autistic, and autistic across
3 severity tiers) and run through fixed scenarios; the resulting conversations are used to
(1) test whether a classifier can recover the persona/severity label from behavior alone,
and (2) score conversations for bias and benchmark multiple LLMs against each other.

---

## 1. Prerequisites

- **Python 3.11+**
- **Node.js** (LTS version) + npm, for the frontend
- API keys for whichever LLMs you're testing against (OpenAI and/or Anthropic)
- Git Bash, WSL, or a Unix-like shell recommended on Windows (some commands below assume
  forward-slash paths — see notes)

---

## 2. Project Structure

```
autism-llm-bias-project/
├── frontend/     — Next.js dashboard (conversations, classifier, features, benchmark pages)
├── backend/      — FastAPI app (simulation engine, classifier, bias scoring, RL bandit)
└── docs/         — synopsis, workflow notes
```

---

## 3. Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows
# venv\Scripts\activate           # Command Prompt
# venv\Scripts\Activate.ps1       # PowerShell (may need: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in your real API keys:
```
DATABASE_URL=sqlite:///./autism_bias.db
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
APP_ENV=development
```

Start the backend:
```bash
uvicorn app.main:app --reload
```

Verify it's running:
```bash
curl http://localhost:8000/health
# → {"status":"ok","environment":"development"}
```

### Frontend

In a separate terminal:
```bash
cd frontend
npm install
```

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the dev server:
```bash
npm run dev
```

Open `http://localhost:3000`. Both the backend (`:8000`) and frontend (`:3000`) need to be
running at the same time for the dashboard to show real data.

---

## 4. Running Simulations — Step by Step

Nothing runs automatically in the background. Each stage below has to be triggered, in order,
for results to appear in the dashboard. You can trigger these individually via the API
(e.g. with `curl` or a tool like Postman), or run the whole chain at once using the benchmark
script (Section 5).

### Step 1 — Generate a conversation
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "group_project_planning", "agent_a_id": "<persona_id>", "agent_b_id": "<persona_id>"}'
```
Returns a `conversation_id`. Persona IDs come from whatever personas have been seeded from
`backend/app/simulation/persona_configs/` into the database.

### Step 2 — Run the post-conversation interview
```bash
curl -X POST http://localhost:8000/conversations/<conversation_id>/interview
```

### Step 3 — Extract behavioral features
```bash
curl -X POST http://localhost:8000/conversations/<conversation_id>/extract-features
```

### Step 4 — Retrain the classifier
Run this after you've generated a meaningful batch of conversations (not after every single
one) — it retrains on all feature data currently in the database:
```bash
curl -X POST http://localhost:8000/classifier/train
```

### Step 5 — Score the conversation for bias
```bash
curl -X POST http://localhost:8000/bias/score/<conversation_id>
```

### Step 6 — Reload the frontend
Results only appear in the dashboard when a page is loaded or refreshed — charts don't
update live while a page is sitting open. Revisit or refresh the relevant page after running
the above steps.

---

## 5. Running the Full Benchmark (recommended way to generate data)

Instead of calling each endpoint by hand, the benchmark script chains simulation → interview
→ feature extraction → bias scoring across every scenario/persona combination for one or more
models:

```bash
cd backend
python scripts/run_benchmark.py --models gpt-4o
```

Start with a single model to confirm everything works before running multiple at once — this
is the most expensive operation in the pipeline (loops the entire chain per scenario/persona
combination) and the one most likely to burn API quota/cost if something's misconfigured.

Once confirmed working, run the full comparison:
```bash
python scripts/run_benchmark.py --models gpt-4o,claude,llama
```

**Note:** check whether `run_benchmark.py` also calls `/classifier/train` as part of its loop.
If it doesn't, retrain the classifier manually (Step 4 above) after the benchmark run
completes, or the classifier page will keep showing stale results from an earlier, smaller
batch of data.

---

## 6. How Results Reflect on the Dashboard

| Dashboard Page | Reflects |
|---|---|
| `/conversations` | Every conversation generated via `/simulate`, across all models/personas run so far |
| `/conversations/[id]` | Full transcript + interview answers + ground-truth vs. predicted label for one conversation |
| `/classifier` | Confusion matrix, accuracy/F1 — only as current as the last `/classifier/train` call |
| `/features` | Behavioral feature values grouped by severity tier, from all conversations with extracted features |
| `/benchmark` | Leaderboard across LLMs — only includes models you've actually run via the benchmark script |
| `/benchmark/[model]` | Per-model bias scores + annotated transcript highlighting deficit/strength language |

**Key thing to remember:** generating more conversations does *not* automatically update the
classifier or bias scores for them — each of those is a separate step (Sections 4–5). If a
page looks stale after running new simulations, check whether you've re-run the classifier
training and bias scoring steps, not just the simulation step.

---

## 7. Typical Workflow for a Fresh Batch of Results

```bash
# 1. Generate data across models
python backend/scripts/run_benchmark.py --models gpt-4o,claude,llama

# 2. Confirm classifier is retrained on the new data (if not automatic in the script)
curl -X POST http://localhost:8000/classifier/train

# 3. Reload the frontend and check all 7 pages
```

---

## 8. Troubleshooting

- **`uvicorn: command not found`** — venv isn't activated, or dependencies weren't installed
  inside it. Re-run `source venv/Scripts/activate` then `pip install -r requirements.txt`.
- **Frontend shows old/mock-looking data** — check the browser console for fetch errors, and
  confirm `NEXT_PUBLIC_API_URL` in `frontend/.env.local` points to the running backend.
- **Classifier results look empty or all one class** — likely not enough conversations
  generated yet, or `/classifier/train` hasn't been called since the last batch of
  simulations.
- **`curl https://localhost:8000/...` fails with a TLS/schannel error** — use `http://`, not
  `https://`; the dev server isn't running TLS.
