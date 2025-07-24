document.getElementById("agentForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const agent = document.getElementById("agentSelect").value;
  const model = document.getElementById("modelSelect").value;
  const input = document.getElementById("inputText").value;
  const outputCard = document.getElementById("outputCard");
  const outputText = document.getElementById("outputText");

  if (!input.trim()) {
    alert("Please enter some input text.");
    return;
  }

  outputText.innerHTML = `<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>`;
  outputCard.style.display = "block";

  try {
    const response = await fetch("http://localhost:8000/api/run-agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_name: agent,
        input_text: input,
        model_name: model || null
      })
    });

    const data = await response.json();
    outputText.innerHTML = `
      <strong>Agent:</strong> ${agent}<br>
      <strong>Model:</strong> ${model || "auto"}<br>
      <strong>Output:</strong><br>
      <em>${data.output}</em>
    `;
    outputCard.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    outputText.innerHTML = `<span class="text-danger">Error: ${error.message}</span>`;
  }
});
