import { copyToClipboard } from "../utils/clipboard.js";
import { showToast } from "../utils/toast.js";
import { fetchDecryptedPassword } from "../api/passwordApi.js";
import { toggleInlinePassword } from "../ui/password/inlineReveal.js";

export function initClickHandlers() {
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
  });
}