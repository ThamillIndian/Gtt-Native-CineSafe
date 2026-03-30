# CineSafe Agent

CineSafe Agent is a specialized AI production analyst that lives in your git repository. It helps film producers and line producers evaluate screenplay feasibility by analyzing risks, budget pressures, and scheduling constraints early in the pre-production phase.

## What it does
- **Structured Scene Breakdown**: Automatically extracts scenes and metadata from raw screenplay text.
- **Risk Analysis**: Scores scenes across 5 pillars (Safety, Logistics, Schedule, Budget, Compliance) using weighted heuristics.
- **Budget Pressure Estimation**: Identifies cost drivers and classifies scenes into pressure bands.
- **Schedule Feasibility**: Detects clustering opportunities and logistical bottlenecks.
- **Scenario Simulation**: Tests the production plan against constraints like budget cuts or accelerated timelines.

## Why it works
Unlike generic LLM wrappers, CineSafe Agent combines **deterministic production logic** (grounded in CSV data) with **LLM-powered explanation**. This ensures consistent, professional-grade results that producers can trust.

## Getting Started

### Prerequisites
- Python 3.10+
- OpenAI/Anthropic/Gemini API Key

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd cinesafe-agent

# Install dependencies
pip install -r requirements.txt
```

### Usage
Run the analysis pipeline on the sample script:
```bash
python -m runtime.pipeline
```

To view the interactive dashboard:
```bash
streamlit run ui/streamlit_app.py
```

## Repository Structure
- `agent.yaml`: Manifest for the GitAgent standard.
- `SOUL.md`: Personality and values of the CineSafe Agent.
- `RULES.md`: Operational constraints.
- `skills/`: Capability definitions for the agent.
- `runtime/`: The core engine, adapters, and data grounding files.
- `ui/`: Streamlit-based user interface.

## Hackathon Compliance
This agent is built for the **GitAgent Hackathon** and follows the **GitAgent Open Standard**.
To validate the structure:
```bash
npx gitagent validate
```
