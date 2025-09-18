//  CONFIGURACIÓN 
const API_URL = "http://localhost:8000/api/secrets";

//  FUNCIONES PRINCIPALES 

// Crear un secreto
async function createSecret() {
    const text = document.getElementById("secretInput").value;
    if (!text) {
        alert("Escribe un secreto primero");
        return;
    }

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            secret: text,
            ttl_seconds: 3600
        }) // 1 hora
    });

    const resultEl = document.getElementById("createResult");
    const copyBtn = document.getElementById("copyBtn");

    if (response.ok) {
        const data = await response.json();
        const url = `http://localhost:8000${data.url}`; // URL completa
        resultEl.textContent = `✅ Secreto guardado. URL: ${url}`;

        // Mostrar botón copiar y guardar URL
        copyBtn.style.display = "inline-block";
        copyBtn.dataset.url = url;
    } else {
        resultEl.textContent = "❌ Error al guardar el secreto";
    }
}

// Revelar un secreto
async function getSecret() {
    let id = document.getElementById("secretId").value.trim();
    const resultEl = document.getElementById("getResult");

    if (!id) {
        alert("Ingresa un ID");
        return;
    }

    // Si el usuario pegó la URL completa, extraemos solo el ID
    if (id.includes("/s/")) {
        id = id.split("/s/")[1].replace("/reveal", "");
    }

    if (!id) {
        resultEl.textContent = "❌ ID o URL no válido.";
        return;
    }

    const response = await fetch(`${API_URL}/${id}/reveal`, {
        method: "POST"
    });

    if (response.status === 404) {
        resultEl.textContent = "❌ Secreto no encontrado o expirado.";
        return;
    }

    if (!response.ok) {
        resultEl.textContent = "❌ Error al revelar el secreto.";
        return;
    }

    const data = await response.json();
    resultEl.textContent = `✅ Secreto: ${data.secret}`;
}

// Copiar URL al portapapeles
function copyURL() {
    const btn = document.getElementById("copyBtn");
    navigator.clipboard.writeText(btn.dataset.url)
        .then(() => alert("URL copiada al portapapeles ✅"))
        .catch(() => alert("Error al copiar URL ❌"));
}