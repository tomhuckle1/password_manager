import { initClickHandlers } from "./handlers/clickHandlers.js";
import { initPasswordModal } from "./ui/password/modal.js";
import { initCategoryDelete } from "./ui/category/delete.js";

document.addEventListener("DOMContentLoaded", () => {
  initPasswordModal();
  initClickHandlers();
  initCategoryDelete();
});