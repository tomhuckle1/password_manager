import { setEyeIcon } from "../../utils/icons.js";

const mask = "••••••••••";
let modal;

export function initPasswordModal() {
  const el = document.getElementById("entryModal");
  if (!el) return;

  modal = new bootstrap.Modal(el);

  el.addEventListener("hidden.bs.modal", () => {
    document.getElementById("modalPasswordMasked").textContent = mask;
    setEyeIcon(document.getElementById("modalTogglePassword"), false);

    el.dataset.entryId = "";
    el.dataset.passwordShown = "false";
    el.dataset.decryptedPassword = "";
  });
}

export function openPasswordModalFromRow(row) {
  const el = document.getElementById("entryModal");
  if (!el) return;

  const id = row.dataset.entryId;
  const admin = row.dataset.isAdmin === "true";

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

  document.getElementById("modalEditBtn").href = `/passwords/${id}/edit`;
  document.getElementById("modalDeleteForm").action = `/passwords/${id}/delete`;

  document.getElementById("modalDeleteBtn")
    ?.classList.toggle("d-none", !admin);

  modal.show();
}