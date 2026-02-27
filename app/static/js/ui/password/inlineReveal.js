import { fetchDecryptedPassword } from "../../api/passwordApi.js";
import { setEyeIcon } from "../../utils/icons.js";
import { showToast } from "../../utils/toast.js";

export async function toggleInlinePassword(id, btn) {
  const box = document.getElementById(`pwbox-${id}`);
  const text = document.getElementById(`pwtext-${id}`);

  if (!box) return;

  // hide
  if (!box.classList.contains("d-none")) {
    box.classList.add("d-none");
    if (text) text.textContent = "";
    setEyeIcon(btn, false);
    showToast("Password hidden");
    return;
  }

  // show
  const pw = await fetchDecryptedPassword(id);
  if (text) text.textContent = pw;
  box.classList.remove("d-none");
  setEyeIcon(btn, true);
  showToast("Password revealed");
}