let cannotModal;
let confirmModal;
let pendingForm;

export function initCategoryDelete() {
  const cannotEl = document.getElementById("cannotDeleteCategoryModal");
  const confirmEl = document.getElementById("confirmDeleteCategoryModal");
  if (!cannotEl || !confirmEl) return;

  cannotModal = new bootstrap.Modal(cannotEl);
  confirmModal = new bootstrap.Modal(confirmEl);

  const confirmBtn = document.getElementById("confirmDeleteCategoryBtn");
  const cannotText = document.getElementById("cannotDeleteCategoryText");
  const confirmText = document.getElementById("confirmDeleteCategoryText");

  confirmBtn.addEventListener("click", () => {
    if (pendingForm) pendingForm.submit();
  });

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-category-delete]");
    if (!btn) return;

    e.preventDefault();

    const form = btn.closest("form");
    if (!form) return;

    const name = btn.dataset.categoryName;
    const count = Number(btn.dataset.categoryCount || 0);

    if (count > 0) {
      if (cannotText)
        cannotText.textContent = `"${name}" contains ${count} password(s).`;

      cannotModal.show();
    } else {
      pendingForm = form;

      if (confirmText)
        confirmText.textContent = `Are you sure you want to delete "${name}"?`;

      confirmModal.show();
    }
  });
}