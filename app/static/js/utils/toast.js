export function showToast(message) {
  const toast = document.createElement("div");
  toast.className =
    "position-fixed bottom-0 end-0 m-3 px-3 py-2 bg-dark text-white rounded shadow";
  toast.style.zIndex = 2000;
  toast.textContent = message;

  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}