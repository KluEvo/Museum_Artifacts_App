document.addEventListener("DOMContentLoaded", () => {
    loadAllArtifacts();
    document.getElementById("artifact-form").addEventListener("submit", handleFormSubmit);
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
                    <button onclick='populateUpdate(${JSON.stringify(a)})'>Edit</button>
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

function getFormData() {
    const id = document.getElementById("artifact-id").value;
    const name = document.getElementById("artifact-name").value.trim();
    const accession = document.getElementById("artifact-accession").value.trim();
    const discovery = document.getElementById("artifact-discovery").value;
    const value = document.getElementById("artifact-value").value;
    const parent = document.getElementById("artifact-parent").value.trim();
    const museum = document.getElementById("artifact-museum").value.trim();

    const discoveryDateIso = discovery ? `${discovery}T00:00:00` : null;

    return {
        id,
        payload: {
            name,
            accession_number: accession,
            discovery_date: discoveryDateIso,
            estimated_value: value ? parseInt(value) : null,
            parent_artifact: parent || null,
            museum_id: museum
        }
    };
}

async function handleFormSubmit(event) {
    event.preventDefault();

    const { id, payload } = getFormData();

    if (!payload.name || !payload.accession_number || !payload.museum_id) {
        document.getElementById("form-output").innerText =
            "Name, Accession Number, and Museum ID are required.";
        return;
    }

    try {
        if (id) {
            await apiFetch(`/artifact/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            document.getElementById("form-output").innerText = "Artifact updated.";
        } else {
            await apiFetch("/artifact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            document.getElementById("form-output").innerText = "Artifact created.";
        }

        resetForm();
        loadAllArtifacts();

    } catch (error) {
        document.getElementById("form-output").innerText = error.message;
    }
}

function populateUpdate(artifact) {
    document.getElementById("form-title").innerText = "Update Artifact";
    document.getElementById("artifact-id").value = artifact.artifact_id;
    document.getElementById("artifact-name").value = artifact.name || "";
    document.getElementById("artifact-accession").value = artifact.accession_number || "";
    document.getElementById("artifact-discovery").value = artifact.discovery_date ? artifact.discovery_date.split("T")[0] : "";
    document.getElementById("artifact-value").value = artifact.estimated_value || "";
    document.getElementById("artifact-parent").value = artifact.parent_artifact || "";
    document.getElementById("artifact-museum").value = artifact.museum_id || "";
}

function resetForm() {
    document.getElementById("form-title").innerText = "Create Artifact";
    document.getElementById("artifact-form").reset();
    document.getElementById("artifact-id").value = "";
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
