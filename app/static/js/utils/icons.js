export function setEyeIcon(btn, isShown) {
  const i = btn?.querySelector("i");
  if (!i) return;
  i.classList.toggle("bi-eye", !isShown);
  i.classList.toggle("bi-eye-slash", isShown);
}