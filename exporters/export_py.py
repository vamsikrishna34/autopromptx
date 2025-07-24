# exporters/export_py.py

def export_to_python(agent_name: str, model_name: str, prompt: str, filepath: str):
    py_content = f"""from transformers import pipeline

model = pipeline("text2text-generation", model="{model_name}")

prompt = \"\"\"{prompt}\"\"\"
result = model(prompt)
print(result[0]["generated_text"])
"""
    with open(filepath, "w") as f:
        f.write(py_content)
