import { fetchDecryptedPassword } from "../../api/passwordApi.js";
import { setEyeIcon } from "../../utils/icons.js";
import { showToast } from "../../utils/toast.js";

const mask = "••••••••••";

export async function toggleModalPassword() {
  const modal = document.getElementById("entryModal");
  const btn = document.getElementById("modalTogglePassword");
  const pwEl = document.getElementById("modalPasswordMasked");
  if (!modal || !btn || !pwEl) return;

  const id = modal.dataset.entryId;
  if (!id) return;

  // Hide
  if (modal.dataset.passwordShown === "true") {
    modal.dataset.passwordShown = "false";
    pwEl.textContent = mask;
    setEyeIcon(btn, false);
    showToast("Password hidden");
    return;
  }

  // Show
  if (!modal.dataset.decryptedPassword) {
    modal.dataset.decryptedPassword = await fetchDecryptedPassword(id);
  }

  modal.dataset.passwordShown = "true";
  pwEl.textContent = modal.dataset.decryptedPassword;
  setEyeIcon(btn, true);
  showToast("Password revealed");
}