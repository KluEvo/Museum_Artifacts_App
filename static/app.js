document.addEventListener("DOMContentLoaded", () => {
    loadArtifactCount();
});

async function loadArtifactCount() {
    try {
        const response = await fetch("/artifact/count");

        if (!response.ok) {
            throw new Error("Failed to fetch artifact count");
        }

        const count = await response.json();
        document.getElementById("artifact-count").innerText = count;

    } catch (error) {
        document.getElementById("artifact-count").innerText = "Error";
        setError(error);
    }
}