import { authService } from '../services/authServices.js';
  
authService.logout();
export class Login {
  constructor() {
    this.initLoginForm();
  }

  initLoginForm() {
    const form = document.querySelector("form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const email = form.querySelector("#email").value.trim();
      const password = form.querySelector("#password").value.trim();

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const containsMaliciousChars = /<|>|'|"|;|--|\/\*/.test(email + password);

      if (!email || !password || !emailRegex.test(email) || containsMaliciousChars) {
        alert("Datos inválidos. Verifica tu información.");
        return;
      }
      
      try {
        const loadingBtn = form.querySelector("button[type='submit']");
        loadingBtn.disabled = true;
        loadingBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Cargando...';

        const data = await authService.login(email, password);
        window.location.href = "chatUser.html";
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