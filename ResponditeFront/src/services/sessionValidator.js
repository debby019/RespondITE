export function validateSession() {
  const user = JSON.parse(localStorage.getItem("user"));
  const token = localStorage.getItem("token");

  if (!user || !token) {
    window.location.href = "index.html";
    return null;
  }

  return {
    usuario_id: user.id,
    role: user.role,
    chat_id: user.chat_id
  };
}
