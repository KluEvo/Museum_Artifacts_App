document.addEventListener("DOMContentLoaded", () => {
    loadAllArtifacts();
});

function renderArtifactsTable(artifacts, containerId) {
    const container = document.getElementById(containerId);
    if (!artifacts || artifacts.length === 0) {
        container.innerHTML = "<p>No artifacts found.</p>";
        return;
    }

    let html = `
        <table border="1" cellpadding="6">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Accession</th>
                <th>Discovery Date</th>
                <th>Estimated Value</th>
                <th>Parent Artifact</th>
                <th>Museum ID</th>
            </tr>
    `;

    artifacts.forEach(a => {
        html += `
            <tr>
                <td>${a.artifact_id}</td>
                <td>${a.name}</td>
                <td>${a.accession_number}</td>
                <td>${formatDate(a.discovery_date)}</td>
                <td>${a.estimated_value ?? "-"}</td>
                <td>${a.parent_artifact ?? "-"}</td>
                <td>${a.museum_id}</td>
            </tr>
        `;
    });

    html += "</table>";
    container.innerHTML = html;
}

function formatDate(dateStr) {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString();
}

async function loadAllArtifacts() {
    const response = await fetch("/artifacts");
    const artifacts = await response.json();
    renderArtifactsTable(artifacts, "artifact-table");
}

async function searchById() {
    const id = document.getElementById("search-id").value.trim();
    if (!id) return;
    const response = await fetch(`/artifact/id?id=${id}`);
    const artifact = await response.json();
    renderArtifactsTable([artifact], "search-results");
}

async function searchByName() {
    const name = document.getElementById("search-name").value.trim();
    if (!name) return;
    const response = await fetch(`/artifact/name?name=${encodeURIComponent(name)}`);
    const artifacts = await response.json();
    renderArtifactsTable(artifacts, "search-results");
}

async function searchByAccession() {
    const accession = document.getElementById("search-accession").value.trim();
    if (!accession) return;
    const response = await fetch(`/artifact/accession?accession=${encodeURIComponent(accession)}`);
    const artifacts = await response.json();
    renderArtifactsTable(artifacts, "search-results");
}
