import { authService } from '../services/authServices.js';

export class Register {
  constructor() {
    this.form = document.querySelector("#registerForm");
    
    if (!this.form) {
      console.error("ERROR: No se encontró el formulario con #registerForm");
      return;
    }
    this.form.onsubmit = this.handleSubmit.bind(this);
  }

  async handleSubmit(e) {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    const contieneCaracteresMaliciosos = /[<>"'`]/.test(nombre + email + password);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!nombre || !email || !password || contieneCaracteresMaliciosos || !emailRegex.test(email)) {
      alert("Datos inválidos. Verifica los campos.");
      return;
    }

    try {
      const response = await authService.register(nombre, email, password);
      alert("¡Registro exitoso!");
      window.location.href = "index.html";
    } catch (err) {
      console.error("Error en el registro:", {
        message: err.message,
        stack: err.stack
      });
      alert("Error: " + (err.message || "Consulta la consola"));
    }
  }
}

new Register();
