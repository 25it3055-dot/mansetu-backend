# MannSetu Backend (FastAPI demo)

This is a runnable backend scaffold for the uploaded MannSetu React prototype.

## 1. Run on macOS

```bash
cd mannsetu_backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open:
- API status: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

## 2. Endpoints

- `GET /health`
- `POST /api/consent`
- `GET /api/consent/{user_id}`
- `POST /api/checkins`
- `GET /api/checkins/{user_id}`
- `GET /api/patterns/{user_id}`
- `GET /api/alerts/{user_id}`
- `POST /api/support/match`
- `GET /api/support/{user_id}`
- `POST /api/followups`
- `GET /api/followups/{user_id}`
- `POST /api/demo/reset`

The default demo user ID is `demo-user`.

## 3. Test the complete flow

Use `/docs` and run these requests in order.

### A. Consent

```json
{
  "user_id": "demo-user",
  "accepted": true,
  "share_peer": true,
  "share_community": true,
  "share_professional": false
}
```

### B. First check-in

```json
{
  "user_id": "demo-user",
  "mood": "calm",
  "energy": 4,
  "connection": 4,
  "stress": 2,
  "note": ""
}
```

Expected: saved, `baseline_needed`, no alert.

### C. Second check-in to demonstrate change

```json
{
  "user_id": "demo-user",
  "mood": "low",
  "energy": 2,
  "connection": 2,
  "stress": 4,
  "note": ""
}
```

Expected: rule-based `change_to_review` and a private alert recommendation. This is an illustrative demo rule, not a clinical assessment.

### D. Ask for peer support

```json
{
  "user_id": "demo-user",
  "support_type": "peer",
  "language": "Hindi",
  "availability": "Now",
  "consent_to_share": true
}
```

Expected: a demo match suggestion. No real person is contacted.

### E. Follow-up

```json
{
  "user_id": "demo-user",
  "choice": "7_days"
}
```

Expected: preference and due date saved in memory. No notification is sent.

## 4. Frontend connection

In React, use `http://127.0.0.1:8000` as the API base URL during local development.

Example:

```js
const API_BASE = "http://127.0.0.1:8000";

const response = await fetch(`${API_BASE}/api/checkins`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: "demo-user",
    mood: "calm",
    energy: 4,
    connection: 4,
    stress: 2,
    note: ""
  })
});

const data = await response.json();
if (!response.ok) throw new Error(data.detail || "Request failed");
```

Important: the uploaded React app currently saves check-ins in browser `localStorage` (`src/data/checkins.js`). To actually use this API, replace that local-only save function with an async `fetch` call, and update consent/follow-up handlers similarly. Merely running this backend does not automatically connect the frontend.

## 5. Important limitations

- This starter uses in-memory dictionaries. Restarting the server clears all data.
- It has no authentication and is intended only for a local hackathon demo with fictional data.
- It does not diagnose, predict depression, send alerts to others, contact support workers, or send scheduled notifications.
- Change detection is a transparent illustrative rule and should be reviewed with the ML teammate before claiming model-based performance.
- Before real users: integrate the database, authentication, secure secrets, access controls, deletion/retention rules, and consent audit logs.
