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
    console.log("Submit detectado - preveniendo acción por defecto");
    e.preventDefault();
    
    try {
      console.log("Obteniendo valores del formulario");
      const nombre = document.getElementById("nombre").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      
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