document.addEventListener("DOMContentLoaded", () => {
    loadAllMuseums();
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

function renderMuseumsTable(museums) {
    const container = document.getElementById("museum-table");
    if (!museums || museums.length === 0) {
        container.innerHTML = "<p>No museums found.</p>";
        return;
    }

    let html = `
        <table border="1" cellpadding="6">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Location</th>
                <th>Contact Email</th>
            </tr>
    `;

    museums.forEach(m => {
        html += `
            <tr>
                <td>${m.museum_id}</td>
                <td>${m.name || ""}</td>
                <td>${m.location || ""}</td>
                <td>${m.contact_email || ""}</td>
            </tr>
        `;
    });

    html += "</table>";
    container.innerHTML = html;
}

async function loadAllMuseums() {
    const container = document.getElementById("museum-table");
    container.innerText = "Loading museums...";
    try {
        const museums = await apiFetch("/museum/all");
        renderMuseumsTable(museums);
    } catch (error) {
        container.innerText = error.message;
    }
}
