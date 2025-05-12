import { api } from './api.js';

export const authService = {
  async login(email, password) {
    const data = await api.post("/login", { email, password });
    
    // Datos de sesión
    localStorage.setItem("token", data.token );
    localStorage.setItem("user", JSON.stringify({
      id: data.usuario_id,
      role: data.rol,
      chat_id: data.chat_id
    }));

    return data;
  },

  async register(nombre, email, password) {
    try {
      const response = await api.post("/register", { 
        nombre, 
        email, 
        password 
      });
      return response;
    } catch (error) {
      console.error("Error en authService.register:", error);
      throw error;
    }
  },

  logout() {
    try {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        console.log("Local storage cleared (logout)");
    } catch (e) {
        console.warn("Failed to clear localStorage:", e);
    }
  },

  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user") || "null");
  },

  isAuthenticated() {
    return !!localStorage.getItem("token");
  }
};