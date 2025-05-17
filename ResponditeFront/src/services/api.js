const API_BASE_URL = "http://127.0.0.1:8000";

export const api = {
  async request(method, endpoint, data = null) {
    const config = {
      method,
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token") || ""}`
      },
    };

    if (data) config.body = JSON.stringify(data);

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`);
    }

    return response.json();
  },

  get(endpoint) {
    return this.request("GET", endpoint);
  },

  post(endpoint, data) {
    return this.request("POST", endpoint, data);
  },

  put(endpoint, data) {
    return this.request("PUT", endpoint, data);
  },

  delete(endpoint) {
    return this.request("DELETE", endpoint);
  }
};