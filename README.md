# AutoPromptX – GPT Prompt Engineering CLI Tool

AutoPromptX is a command-line tool that helps developers prototype, test, and manage prompts for GPT models. It's designed to mimic real-world prompt iteration needs with organized template handling and basic configuration separation.

---

## ✨ Features

- Save and reuse prompts using text-based templates
- Modular prompt chaining support
- CLI interface for quick test runs and feedback
- Simple config module for managing keys/settings
- Designed with students and early professionals in mind

---

## 🧰 Technologies

- Python
- OpenAI API
- CLI (Command-line interface)
- Regular expressions
- Modular scripting (with `config.py` and templates)

---

## 📁 Folder Structure

```
AutoPromptX/
├── autopromptx.py
├── config.py
├── prompt_templates/
│   ├── greeting.txt
│   └── summary.txt
└── README.md
```

---

## 🚀 How to Run

```bash
pip install openai
export OPENAI_API_KEY=your_key_here
python autopromptx.py
```

---

## 💬 Sample Prompts

Templates are stored in `/prompt_templates/`. You can edit or add your own to keep prompts organized.

---

## 👥 Audience

Ideal for students, AI learners, and junior developers exploring GenAI workflows.

---

## 📦 Future Ideas

- Streamlit GUI wrapper
- VS Code extension for inline prompt testing
- Prompt version control & analytics
