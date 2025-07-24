document.getElementById("agentForm").addEventListener("submit", function (e) {
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

  // Show loading spinner
  outputText.innerHTML = `<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>`;
  outputCard.style.display = "block";

  // Simulate processing delay
  setTimeout(() => {
    const output = `
      <strong>Agent:</strong> ${agent}<br>
      <strong>Model:</strong> ${model || "auto"}<br>
      <strong>Output:</strong><br>
      <em>[Mocked response for "${input}"]</em>
    `;
    outputText.innerHTML = output;

    // Optional: scroll to output
    outputCard.scrollIntoView({ behavior: "smooth" });
  }, 1000);
});

// Enable Bootstrap tooltips
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
  new bootstrap.Tooltip(el);
});
