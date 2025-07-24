document.getElementById("agentForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const agent = document.getElementById("agentSelect").value;
  const model = document.getElementById("modelSelect").value;
  const input = document.getElementById("inputText").value;

  if (!input.trim()) {
    alert("Please enter some input text.");
    return;
  }

  const output = `
    <strong>Agent:</strong> ${agent}<br>
    <strong>Model:</strong> ${model || "auto"}<br>
    <strong>Output:</strong><br>
    <em>[Mocked response for "${input}"]</em>
  `;

  document.getElementById("outputText").innerHTML = output;
  document.getElementById("outputCard").style.display = "block";
});
