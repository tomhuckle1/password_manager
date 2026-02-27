export async function fetchDecryptedPassword(entryId) {
  const res = await fetch(`/api/password/${entryId}/password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || "Permission denied");
  }

  return (await res.json()).password;
}