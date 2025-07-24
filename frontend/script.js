document.getElementById("agentForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const agent = document.getElementById("agentSelect").value;
  const model = document.getElementById("modelSelect").value;
  const input = document.getElementById("inputText").value;

  // Mock output for now
  const output = `Agent: ${agent}\nModel: ${model || "auto"}\nOutput: [Mocked response for "${input}"]`;

  document.getElementById("outputText").textContent = output;
  document.getElementById("outputCard").style.display = "block";
});
