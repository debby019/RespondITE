import { authService } from '../services/authServices.js';

export class Login {
  constructor() {
    this.initLoginForm();
  }

  initLoginForm() {
    const form = document.querySelector("form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const email = form.querySelector("#email").value.trim();
      const password = form.querySelector("#password").value;

      try {
        const loadingBtn = form.querySelector("button[type='submit']");
        loadingBtn.disabled = true;
        loadingBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Cargando...';

        const data = await authService.login(email, password);
        window.location.href = data.role === "admin" ? "ChatAdmin.html" : "ChatUser.html";
      } catch (error) {
        alert(error.message);
        form.querySelector("#password").value = "";
      } finally {
        const submitBtn = form.querySelector("button[type='submit']");
        submitBtn.disabled = false;
        submitBtn.textContent = "Iniciar sesión";
      }
    });
  }
}