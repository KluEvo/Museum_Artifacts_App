document.addEventListener("DOMContentLoaded", () => {
    loadAllArtifacts();
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

function formatDate(dateStr) {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString();
}

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
                <th>Actions</th>
            </tr>
    `;

    artifacts.forEach(a => {
        html += `
            <tr>
                <td>${a.artifact_id}</td>
                <td>${a.name}</td>
                <td>${a.accession_number}</td>
                <td>${formatDate(a.discovery_date)}</td>
                <td>${a.estimated_value || ""}</td>
                <td>${a.parent_artifact || ""}</td>
                <td>${a.museum_id}</td>
                <td>
                    <button onclick="deleteArtifact('${a.artifact_id}')">Delete</button>
                    <button onclick="populateUpdate('${a.artifact_id}','${a.name}','${a.accession_number}','${a.discovery_date}','${a.estimated_value}','${a.parent_artifact}','${a.museum_id}')">Edit</button>
                </td>
            </tr>
        `;
    });

    html += "</table>";
    container.innerHTML = html;
}

async function loadAllArtifacts() {
    try {
        const artifacts = await apiFetch("/artifact/all");
        renderArtifactsTable(artifacts, "artifact-table");
    } catch (error) {
        document.getElementById("artifact-output").innerText = error.message;
    }
}

async function createArtifact() {
    const name = document.getElementById("create-name").value.trim();
    const accession = document.getElementById("create-accession").value.trim();
    const discovery = document.getElementById("create-discovery").value;
    const value = document.getElementById("create-value").value;
    const parent = document.getElementById("create-parent").value.trim();
    const museum = document.getElementById("create-museum").value.trim();

    if (!name || !accession || !museum) {
        document.getElementById("create-output").innerText = 
            "Name, Accession Number, and Museum ID are required.";
        return;
    }

    const discoveryDateIso = discovery ? `${discovery}T00:00:00` : null;

    const payload = {
        name: name,
        accession_number: accession,
        discovery_date: discoveryDateIso,
        estimated_value: value ? parseInt(value) : null,
        parent_artifact: parent || null,
        museum_id: museum
    };

    try {
        await apiFetch("/artifact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        document.getElementById("create-output").innerText = "Artifact created.";
        loadAllArtifacts();

    } catch (error) {
        document.getElementById("create-output").innerText = error.message;
    }
}


async function deleteArtifact(id) {
    try {
        await apiFetch(`/artifact?id=${id}`, {
            method: "DELETE"
        });

        loadAllArtifacts();
    } catch (error) {
        document.getElementById("artifact-output").innerText = error.message;
    }
}

async function searchById() {
    const id = document.getElementById("search-id").value.trim();
    if (!id) return;

    try {
        const artifact = await apiFetch(`/artifact/id?id=${id}`);
        renderArtifactsTable([artifact], "search-results");
    } catch (error) {
        document.getElementById("search-results").innerText = error.message;
    }
}

async function searchByName() {
    const name = document.getElementById("search-name").value.trim();
    if (!name) return;

    try {
        const artifacts = await apiFetch(`/artifact/name?name=${encodeURIComponent(name)}`);
        renderArtifactsTable(artifacts, "search-results");
    } catch (error) {
        document.getElementById("search-results").innerText = error.message;
    }
}

async function searchByAccession() {
    const accession = document.getElementById("search-accession").value.trim();
    if (!accession) return;

    try {
        const artifacts = await apiFetch(`/artifact/accession?accession=${encodeURIComponent(accession)}`);
        renderArtifactsTable(artifacts, "search-results");
    } catch (error) {
        document.getElementById("search-results").innerText = error.message;
    }
}

function populateUpdate(id, name, accession, discovery, value, parent, museum) {
    const newName = prompt("Enter new name:", name);
    if (newName === null) return;

    const newAccession = prompt("Enter new accession number:", accession);
    if (newAccession === null) return;

    const newDiscovery = prompt("Enter new discovery date (YYYY-MM-DD):", discovery ? discovery.split('T')[0] : "");
    if (newDiscovery === null) return;

    const newValue = prompt("Enter new estimated value:", value ?? "");
    if (newValue === null) return;

    const newParent = prompt("Enter new parent artifact ID (or leave blank):", parent ?? "");
    if (newParent === null) return;

    const newMuseum = prompt("Enter new museum ID:", museum);
    if (newMuseum === null) return;

    const discoveryDateIso = newDiscovery ? `${newDiscovery}T00:00:00` : null;

    const payload = {
        name: newName,
        accession_number: newAccession,
        discovery_date: discoveryDateIso,
        estimated_value: newValue ? parseInt(newValue) : null,
        parent_artifact: newParent || null,
        museum_id: newMuseum
    };

    apiFetch(`/artifact/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).then(() => {
        document.getElementById("artifact-output").innerText = "Artifact updated.";
        loadAllArtifacts();
    }).catch(err => {
        document.getElementById("artifact-output").innerText = err.message;
    });
}
