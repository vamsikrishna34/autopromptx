# exporters/export_md.py

def export_to_markdown(agent_name: str, model_name: str, output: str, filepath: str):
    md_content = f"""# AutoPromptX Output

**Agent:** {agent_name}  
**Model:** {model_name}  

---

**Output:**  
{output}
"""
    with open(filepath, "w") as f:
        f.write(md_content)
