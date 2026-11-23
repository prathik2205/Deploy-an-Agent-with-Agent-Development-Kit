# Agent Development Kit: Multi-Agent Paint Assistant on Google Cloud

A multi-agent shopping assistant built with the **Agent Development Kit (ADK)**, grounded on product data with **Agent Search**, deployed to **Agent Runtime** (Vertex AI Agent Engine), and exposed through a **Chainlit** web UI.

Scenario: Cymbal Shops, a retail chain, launches a paint department. The agent guides DIY customers from product selection to a priced shopping basket.

## What it does

1. Answers paint questions grounded on a product datasheet PDF (RAG via Agent Search).
2. Lets the customer pick a product line and colours per room.
3. Estimates wall area from room dimensions (doors and windows subtracted).
4. Calculates litres, bucket count and total price across multiple rooms.

## Architecture

```
Chainlit UI ──► Agent Runtime (deployed ADK app)
                      │
                paint_agent (root)
                ├── tool: AgentTool(paint_searcher_agent) ──► Agent Search (datasheet PDF)
                ├── tool: set_session_value ──► session state
                └── sub-agent: room_planner_agent
                                 └── sub-agent: coverage_calculator_agent
```

## Key engineering points

- **Search tool isolation.** Gemini rejects requests that mix a search tool with other tools or implicit `transfer_to_agent` calls (`400 INVALID_ARGUMENT: Multiple tools are supported only when they are all search tools`). The search agent is wrapped in `AgentTool` so it runs in its own isolated call.
- **Shared session state.** `set_session_value` writes `SELECTED_PAINT`, `COVERAGE_RATE` and `PRICE` into `ToolContext.state`.
- **Optional state templating.** Sub-agent instructions use `{KEY?}` so missing keys resolve to empty instead of raising errors.
- **Least-privilege IAM.** The AI Platform Reasoning Engine Service Agent is granted only *Vertex AI User* and *Discovery Engine User*.

## Tech stack

Python, Google ADK, Vertex AI Agent Engine, Agent Search (Discovery Engine), Gemini, Cloud Storage, IAM, Chainlit.

## Project structure

```
paint_agent/            # ADK app (root agent, tools, sub-agents)
chainlit_ui/app.py      # Web front end for the deployed agent
scripts/deploy.sh       # Deployment helper
.env.example            # Required configuration
```

## Setup

### 1. Agent Search data store and app
In the Google Cloud console create a **Custom search (general)** app (`global` location) with a Cloud Storage data store importing the paint datasheet PDF. Use the **Layout Parser**, enable table annotation, and include ancestor headings in chunks. Note the app ID.

### 2. Local environment
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values
cp .env paint_agent/.env
```

### 3. Run locally
```bash
adk run paint_agent                                   # CLI
adk web                                               # Dev UI with State tab
```

### 4. Deploy
```bash
./scripts/deploy.sh
```
Then, in **IAM & Admin > IAM** (enable *Include Google-provided role grants*), grant the Reasoning Engine Service Agent (`service-<PROJECT_NUMBER>@gcp-sa-aiplatform-re.iam.gserviceaccount.com`) the roles **Vertex AI User** and **Discovery Engine User**.

### 5. Query the deployed agent
Add the printed resource name to `.env`:
```
AGENT_RESOURCE_NAME=projects/<id>/locations/<region>/reasoningEngines/<id>
```
```bash
cd chainlit_ui && chainlit run app.py
```

## Example conversation

| User | Agent |
|---|---|
| hello / yes | Summarises the four paint lines |
| I'd like Forever Paint | Shows swatches, asks about rooms |
| Two rooms: living room and baby's room | Asks for colours |
| Living room 5m x 4m, 2.5m high, 1 door, 3 windows | 38.5 m² per coat |
| Always two coats | 77 m², 4 buckets, €160.00 |
| Baby's room 3m x 3m, 2.5m high, 1 door, 1 window | 53 m², 3 buckets, €120.00 (total €280.00) |

## Skills demonstrated

Multi-agent design, RAG grounding, tool orchestration, agent state management, cloud deployment, IAM least privilege, and building a conversational front end.

## Acknowledgement

Based on a Google Cloud Skills Boost challenge lab. All code here is my own implementation.
