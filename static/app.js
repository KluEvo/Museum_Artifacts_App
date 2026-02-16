document.addEventListener("DOMContentLoaded", () => {
    loadArtifactCount();
});

async function apiFetch(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Request failed");
    }

    if (response.status === 204) return null;

    return response.json();
}

async function loadArtifactCount() {
    const output = document.getElementById("data");
    const countEl = document.getElementById("artifact-count");

    try {
        countEl.innerText = "Loading...";
        const count = await apiFetch("/artifact/count");
        countEl.innerText = count;
        output.innerText = "Artifact count loaded successfully.";
    } catch (error) {
        countEl.innerText = "Error";
        output.innerText = error.message;
    }
}
