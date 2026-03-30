# 🎬 CineSafe Agent: Your Git-Native Production Analyst

CineSafe Agent is a specialized AI production analyst designed for the **GitAgent Hackathon**. It lives directly in your repository as a **Git-Native agent**, providing film producers with professional-grade risk, budget, and schedule analysis from raw screenplays.

![CineSafe Dashboard](https://raw.githubusercontent.com/ThamillIndian/Gtt-Native-CineSafe/main/ui/assets/dashboard_preview.png)
*(Replace with your actual screenshot path after uploading to GitHub)*

## 🌟 Key Features
- **🎯 Professional Script Ingestion**: Supports both `.txt` and `.pdf` files. Robustly handles complex **shooting script numbering** (e.g., `4.1`, `4.2`).
- **🛡️ Deterministic Risk Engine**: Grounded in weighted CSV heuristics (`runtime/data/risk_weights.csv`) to provide consistent, safety-first scoring.
- **💰 Budget Pressure Analysis**: Detects high-cost factors (Night shoots, Crowds, Remote locations) and provides actionable "Producer Tips."
- **📊 Interactive Dashboard**: A sleek **Streamlit** interface for visualizing scene-by-scene hotspots and executive summaries.
- **📜 Deep Debugging**: Detailed production logs for every internal step, from regex parsing to LLM reasoning.
- **🤖 Powered by Gemini 2.5 Flash**: Optimized for speed and sophisticated creative reasoning.

## 🏗️ GitAgent Open Standard Compliance
CineSafe is built strictly according to the **GitAgent standard**:
- **`agent.yaml`**: The manifest defining skills and model preferences.
- **`SOUL.md`**: Defines the agent's identity as a meticulous Line Producer.
- **`RULES.md`**: Sets boundaries for deterministic scoring and safety advice.
- **`skills/`**: Fully documented `SKILL.md` files for every agent capability.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Google Gemini API Key

### 2. Installation
```powershell
# Clone the repo
git clone https://github.com/ThamillIndian/Gtt-Native-CineSafe.git
cd Gtt-Native-CineSafe

# Setup Environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Running the Agent
**To see it in action (Manual UI):**
```powershell
pip install -r requirements.txt
streamlit run ui/streamlit_app.py
```

**To validate for GitAgent:**
```powershell
npx @open-gitagent/gitagent validate
```

## 📂 Project Structure
- `runtime/`: The core engine and modular adapters.
- `skills/`: Mandatory skill documentation for GitClaw.
- `ui/`: The interactive analysis dashboard.
- `examples/`: Sample scripts and templates.

---
Built with ❤️ for the **GitAgent Hackathon** by **ThamillIndian**.
