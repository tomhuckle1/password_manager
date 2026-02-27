import { initClickHandlers } from "./handlers/clickHandlers.js";
import { initPasswordModal } from "./ui/password/modal.js";

document.addEventListener("DOMContentLoaded", () => {
  initPasswordModal();
  initClickHandlers();
});