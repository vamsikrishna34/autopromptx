# AutoPromptX

AutoPromptX is a modular, multi-agent GenAI orchestration tool built with Hugging Face Transformers, Bootstrap 5 frontend, and robust fallback logic. It supports CLI execution, dynamic model selection, realistic dummy outputs, and LangChain-style exports — designed for real-world impact and recruiter visibility.

---

## Features

- Multi-agent architecture (Summarizer, Reviewer, Persona, etc.)
- CLI and Bootstrap 5 frontend
- Auto/manual model selection
-  Multi-model fallback with realistic dummy outputs
-  Token diagnostics and similarity scoring
-  Agent planner via Flan-T5
-  LangChain-style export formats (JSON, Markdown, Python)
-  Reusable workflows (`workflows/` folder)

---

## 📦 Folder Structure

```bash
autopromptx/
├── agents/             # Modular agent classes
├── models/             # Model router and fallback logic
├── cli/                # CLI runner
├── utils/              # Validators, diagnostics, dummy outputs
├── planner/            # Agent planner (Flan-T5)
├── exporters/          # Export formats
├── config/             # Config files (models, prompts)
├── frontend/           # Bootstrap 5 UI
├── workflows/          # Saved chains
├── tests/              # Unit tests
├── requirements.txt    # Dependencies
└── README.md           # This file

Quick Start
1. Install dependencies
bash
pip install -r requirements.txt
2. Run from CLI
bash
python cli/run_chain.py --agent SummarizerAgent --input "Your text here" --mode auto
3. Launch frontend (static)
Open frontend/index.html in your browser.

Example Agents
Agent-	Task
SummarizerAgent-	Summarizes input text
CodeReviewerAgent-	Reviews and improves code
PersonaAgent-	Adjusts tone/style
FollowUpAgent-	Suggests next steps
ClarityAgent-	Scores and simplifies text

Model Selection
Auto Mode: System selects best model based on agent/task
Manual Mode: User specifies model via CLI or frontend

Fallback Logic
If a model fails or output is invalid:
Tries fallback models from agent_fallbacks.json
Returns realistic dummy output if all fail

Export Formats
export_json.py → .json
export_md.py → .md
export_py.py → LangChain-style .py

Agent Planner
Use planner/chain_planner.py to suggest agent sequences based on goals:
python
planner = ChainPlanner()
planner.suggest_chain("Summarize and improve clarity")

Testing
bash
pytest tests/