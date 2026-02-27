import { copyToClipboard } from "../utils/clipboard.js";
import { showToast } from "../utils/toast.js";
import { fetchDecryptedPassword } from "../api/passwordApi.js";
import { openPasswordModalFromRow } from "../ui/password/modal.js";
import { toggleInlinePassword } from "../ui/password/inlineReveal.js";
import { toggleModalPassword } from "../ui/password/reveal.js";

export function initClickHandlers() {

  // Modal actions
  document.getElementById("modalCopyUsername")?.addEventListener("click", async () => {
    const text = document.getElementById("modalUsername")?.textContent;
    if (!text) return;
    await copyToClipboard(text);
    showToast("Username copied");
  });

  document.getElementById("modalCopyUrl")?.addEventListener("click", async () => {
    const text = document.getElementById("modalWebsite")?.textContent;
    if (!text) return;
    await copyToClipboard(text);
    showToast("URL copied");
  });

  document.getElementById("modalCopyPassword")?.addEventListener("click", async () => {
    const modal = document.getElementById("entryModal");
    if (!modal?.dataset.entryId) return;

    if (!modal.dataset.decryptedPassword) {
      modal.dataset.decryptedPassword =
        await fetchDecryptedPassword(modal.dataset.entryId);
    }

    await copyToClipboard(modal.dataset.decryptedPassword);
    showToast("Password copied");
  });

  document.getElementById("modalTogglePassword")?.addEventListener("click", async (e) => {
    e.preventDefault();
    await toggleModalPassword();
  });

  // Dashboard actions
  document.addEventListener("click", async (e) => {
    const copyUser = e.target.closest("[data-copy-username]");
    if (copyUser) {
      await copyToClipboard(copyUser.dataset.copyUsername);
      showToast("Username copied");
      return;
    }

    const copyUrl = e.target.closest("[data-copy-url]");
    if (copyUrl) {
      await copyToClipboard(copyUrl.dataset.copyUrl);
      showToast("URL copied");
      return;
    }

    const toggle = e.target.closest("[data-toggle-password]");
    if (toggle) {
      await toggleInlinePassword(toggle.dataset.togglePassword, toggle);
      return;
    }

    const copyPw = e.target.closest("[data-copy-password]");
    if (copyPw) {
      const pw = await fetchDecryptedPassword(copyPw.dataset.copyPassword);
      await copyToClipboard(pw);
      showToast("Password copied");
      return;
    }

    // Open modal on row click, apart from action buttons
    const row = e.target.closest(".vault-row");
    if (row) {
      if (e.target.closest("[data-stop-row-click]")) return;
      openPasswordModalFromRow(row);
    }
  });
}