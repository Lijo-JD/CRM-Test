const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || 'Request failed');
  }

  return response.json() as Promise<T>;
}

export default api;
