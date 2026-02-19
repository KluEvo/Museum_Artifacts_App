document.addEventListener("DOMContentLoaded", () => {
    loadAllLoans();
    document.getElementById("loan-form").addEventListener("submit", handleFormSubmit);
    document.getElementById("cancel-btn").addEventListener("click", resetForm);
    document.getElementById("search-btn").addEventListener("click", searchLoanById);
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
    return new Date(dateStr).toLocaleString();
}

function renderLoansTable(loans, containerId) {
    const container = document.getElementById(containerId);
    if (!loans || loans.length === 0) {
        container.innerHTML = "<p>No loans found.</p>";
        return;
    }

    let html = `
        <table>
            <tr>
                <th>Loan ID</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Status</th>
                <th>Insurance</th>
                <th>To Museum</th>
                <th>From Museum</th>
                <th>Actions</th>
            </tr>
    `;

    loans.forEach(loan => {
        html += `
            <tr>
                <td>${loan.loan_id}</td>
                <td>${formatDate(loan.start_date)}</td>
                <td>${formatDate(loan.end_date)}</td>
                <td>${loan.loan_status || ""}</td>
                <td>${loan.insurance_value || ""}</td>
                <td>${loan.to_museum_id}</td>
                <td>${loan.from_museum_id}</td>
                <td>
                    <button data-id="${loan.loan_id}" class="edit-btn">Edit</button>
                    <button data-id="${loan.loan_id}" class="delete-btn">Delete</button>
                </td>
            </tr>
        `;
    });

    html += "</table>";
    container.innerHTML = html;

    container.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const loan = await apiFetch(`/loan/id?id=${btn.dataset.id}`);
            populateUpdate(loan);
        });
    });

    container.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            await deleteLoan(btn.dataset.id);
            loadAllLoans();
        });
    });
}

async function loadAllLoans() {
    try {
        const loans = await apiFetch("/loan/all");
        renderLoansTable(loans, "loan-output");
    } catch (error) {
        document.getElementById("loan-output").innerText = error.message;
    }
}

function getFormData() {
    return {
        id: document.getElementById("loan-id").value,
        payload: {
            start_date: document.getElementById("loan-start-date").value || null,
            end_date: document.getElementById("loan-end-date").value || null,
            loan_status: document.getElementById("loan-status").value.trim(),
            insurance_value: document.getElementById("loan-insurance").value.trim(),
            to_museum_id: document.getElementById("loan-to-museum").value.trim(),
            from_museum_id: document.getElementById("loan-from-museum").value.trim()
        }
    };
}

async function handleFormSubmit(event) {
    event.preventDefault();
    const { id, payload } = getFormData();

    if (!payload.to_museum_id || !payload.from_museum_id) {
        document.getElementById("form-output").innerText = "Both museum IDs are required.";
        return;
    }

    try {
        if (id) {
            await apiFetch(`/loan/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            document.getElementById("form-output").innerText = "Loan updated.";
        } else {
            await apiFetch("/loan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            document.getElementById("form-output").innerText = "Loan created.";
        }
        resetForm();
        loadAllLoans();
    } catch (error) {
        document.getElementById("form-output").innerText = error.message;
    }
}

function populateUpdate(loan) {
    document.getElementById("form-title").innerText = "Update Loan";
    document.getElementById("loan-id").value = loan.loan_id;
    document.getElementById("loan-start-date").value = loan.start_date ? loan.start_date.split(".")[0] : "";
    document.getElementById("loan-end-date").value = loan.end_date ? loan.end_date.split(".")[0] : "";
    document.getElementById("loan-status").value = loan.loan_status || "";
    document.getElementById("loan-insurance").value = loan.insurance_value || "";
    document.getElementById("loan-to-museum").value = loan.to_museum_id || "";
    document.getElementById("loan-from-museum").value = loan.from_museum_id || "";
}

function resetForm() {
    document.getElementById("form-title").innerText = "Create Loan";
    document.getElementById("loan-form").reset();
    document.getElementById("loan-id").value = "";
}

async function deleteLoan(id) {
    await apiFetch(`/loan?id=${id}`, { method: "DELETE" });
}

async function searchLoanById() {
    const id = document.getElementById("search-loan-id").value.trim();
    if (!id) return;
    try {
        const loan = await apiFetch(`/loan/id?id=${id}`);
        renderLoansTable([loan], "search-results");
    } catch (error) {
        document.getElementById("search-results").innerText = error.message;
    }
}
