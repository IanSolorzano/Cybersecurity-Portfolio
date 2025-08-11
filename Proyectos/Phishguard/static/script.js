/**
 * Send URL to backend for phishing prediction
 */
function checkURL() {
  const inputField = document.getElementById("urlInput");
  const urlToTest = inputField.value.trim();

  if (!urlToTest) {
    displayResult("Por favor ingresa una URL válida.", "text-warning");
    return;
  }

  fetch("/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: urlToTest })
  })
    .then(async response => {
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Error desconocido");
      }

      const message = data.prediction === 1
        ? "¡Atención! Posible phishing detectado."
        : "URL segura.";
      const styleClass = data.prediction === 1 ? "text-danger" : "text-success";
      displayResult(message, styleClass);
    })
    .catch(err => {
      console.error(err);
      displayResult(err.message || "Error de conexión.", "text-danger");
    });
}

function displayResult(text, cssClass) {
  const resultElem = document.getElementById("result");
  resultElem.textContent = text;
  resultElem.className = cssClass + " fw-bold mt-3";
}
