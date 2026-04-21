const API_URL = import.meta.env.VITE_API_URL || "";

export async function fetchGraph(accessToken) {
  const response = await fetch(`${API_URL}/graph`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to load graph");
  }
  return response.json();
}
