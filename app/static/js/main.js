import { initClickHandlers } from "./handlers/clickHandlers.js";
import { initPasswordModal } from "./ui/password/modal.js";
import { initCategoryDelete } from "./ui/category/delete.js";
import "./ui/auth/passwordStrength.js";

document.addEventListener("DOMContentLoaded", () => {
  initPasswordModal();
  initClickHandlers();
  initCategoryDelete();
});