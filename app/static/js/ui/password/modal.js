import { setEyeIcon } from "../../utils/icons.js";

// Mask shown when password is hidden
const mask = "••••••••••";
let modal;

export function initPasswordModal() {
  const el = document.getElementById("entryModal");
  if (!el) return;

  // Create modal
  modal = new bootstrap.Modal(el);

  el.addEventListener("hidden.bs.modal", () => {
    // Reset masked password display
    document.getElementById("modalPasswordMasked").textContent = mask;
    // Reset eye icon to "hidden" state
    setEyeIcon(document.getElementById("modalTogglePassword"), false);

    // Clear state
    el.dataset.entryId = "";
    el.dataset.passwordShown = "false";
    el.dataset.decryptedPassword = "";
  });
}

export function openPasswordModalFromRow(row) {
  const el = document.getElementById("entryModal");
  if (!el) return;

  // Read data
  const id = row.dataset.entryId;
  const admin = row.dataset.isAdmin === "true";

  // Set state
  el.dataset.entryId = id;
  el.dataset.passwordShown = "false";
  el.dataset.decryptedPassword = "";

  document.getElementById("modalTitle").textContent =
    row.dataset.entryName || "Password";

  document.getElementById("modalWebsiteHeader").textContent =
    row.dataset.entryWebsite || "";

  document.getElementById("modalUsername").textContent =
    row.dataset.entryUsername || "";

  document.getElementById("modalWebsite").textContent =
    row.dataset.entryWebsite || "";

  document.getElementById("modalNotes").textContent =
    row.dataset.entryNotes || "";

  document.getElementById("modalUpdated").textContent =
    row.dataset.entryUpdated || "—";

  document.getElementById("modalCreated").textContent =
    row.dataset.entryCreated || "—";

  document.getElementById("modalPasswordMasked").textContent = mask;
  setEyeIcon(document.getElementById("modalTogglePassword"), false);

  // Edit and delete links
  document.getElementById("modalEditBtn").href = `/passwords/${id}/edit`;
  document.getElementById("modalDeleteForm").action = `/passwords/${id}/delete`;

  // Show delete button only if user is admin
  document.getElementById("modalDeleteBtn")
    ?.classList.toggle("d-none", !admin);

  modal.show();
}