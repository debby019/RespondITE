import { authService } from '../services/authServices.js';

authService.logout();


export async function Invitado() {
  try {
    const response = await fetch("http://127.0.0.1:8000/auth/guest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("No se pudo iniciar sesión como invitado.");
    }

    const data = await response.json();

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify({
      id: data.user_id,
      role: "guest",
      chat_id: null
    }));

    window.location.href = "chatUser.html";
  } catch (error) {
    alert("Error al ingresar como invitado: " + error.message);
  }
}

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