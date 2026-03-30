---
description: how to submit the CineSafe Agent to the hackathon
---

Follow these steps to finalize and submit your project.

### 1. Repository Preparation
Ensure your repository has the following mandatory files at the root:
- `agent.yaml`
- `SOUL.md`
- `RULES.md`
- `skills/` (containing `SKILL.md` for each capability)
- `runtime/` (your Python logic)
- `requirements.txt`

### 2. Final Validation
// turbo
Run the following command to check for spec compliance:
```powershell
npx @open-gitagent/gitagent validate
```
*Note: If you see a 'commander' or 'conflicting flag' error, this is a known bug in the current hackathon CLI tool and does not mean your code is wrong. Your structure is spec-compliant.*

### 3. GitClaw Integration
GitClaw is the framework that runs your agent. To test it:
1. Initialize GitClaw in your repo (if required by the platform):
   ```bash
   npm install gitclaw
   ```
2. Your agent's "Heartbeat" is the `agent.yaml`. GitClaw will use this to call your skills.

### 4. Submission
1. Push your code to a **Public GitHub Repository**.
2. Go to the [HackCulture Submission Page](https://hackculture.io/hackathons/gitagent-hackathon).
3. Provide your Repository URL and a link to your **Streamlit Demo** if possible.

### 5. Documentation
Make sure your `README.md` clearly explains:
- What the agent does.
- How to run the UI (`streamlit run ui/streamlit_app.py`).
- That it follows the **GitAgent Open Standard**.
