import { chatService } from '../services/chatServices.js';
import { authService } from '../services/authServices.js';
import { validateSession } from '../services/sessionValidator.js';

window.addEventListener("DOMContentLoaded", () => {

    // Validar que haya una sesión activa y obtener datos del usuario
  const userData = validateSession();

  if (!userData) return;

  const { usuario_id, role, chat_id } = userData;

  new ChatInterface();  
});

export class ChatInterface {
  constructor() {
    // Verificar que el usuario este autenticado o que haya ingresado como invitado.
    if (!authService.isAuthenticated()) {
      const token = localStorage.getItem("token");
      if (token !== "guest-token") {
        window.location.href = "index.html";
        return;
      }
    }

    this.currentUser = authService.getCurrentUser();

  if (!this.currentUser?.id && this.currentUser?.id !== "guest") {
    authService.logout();
    window.location.href = "index.html";
    return;
  }

  // Datos iniciales para la aplicación Vue
    const vueData = {
      fecha: new Date().toLocaleDateString('es-MX', { 
        day: '2-digit', 
        month: 'long', 
        year: 'numeric' 
      }),
      nuevoMensaje: '',
      mensajes: [], // Historial de mensajes del chat actual
      chats: [],   // Lista de chats del usuario
      chatSeleccionado: null,
      chat_id: null, 
      enviando: false,
      usuario_id: this.currentUser.id, // Usuario estudiante/comun.
      esInvitado: this.currentUser.role === 'guest', // Usuario invitado.
      esAdmin: this.currentUser.role === 'admin', // Usuario administrador
    };

    this.initVueApp(vueData);
  }

  initVueApp(initialData) {
    this.app = Vue.createApp({
      data() {
        return initialData; 
      },
      methods: {
        // Carga la lista de chats del usuario.
        async cargarHistorialChats() {
          try {
            const historial = await chatService.getUserChats();
            this.chats = historial;
          } catch (error) {
            console.error("Error al cargar historial:", error);
          }
        },

        async seleccionarChat(chat) {
          this.chat_id = chat.id_chat;
          this.chatSeleccionado = chat.id_chat;
          await this.cargarMensajes();
        },

        // Carga los mensajes de un chat específico
        async cargarMensajes() {
          if (!this.chat_id) return;
          try {
            const mensajes = await chatService.getChatHistory(this.chat_id);
            this.mensajes = mensajes.map(msg => ({
              texto: msg.mensaje,
              tipo: msg.remitente === 'usuario' ? 'usuario' : 'ia',
              timestamp: msg.fecha_envio
            }));
            this.scrollToBottom();
          } catch (error) {
            console.error("Error al cargar mensajes:", error);
          }
        },

      // Enviar un mensaje escrito por el usuario.
        async enviarMensaje() {
          if (!this.nuevoMensaje.trim() || this.enviando) return;

          try {
            this.enviando = true;

            // Si no hay un chat seleccionado crea uno nuevo.
            if (!this.chat_id) {
              const res = await chatService.createNewChat();
              this.chat_id = res.id_chat;
              this.chatSeleccionado = res.id_chat;
              this.mensajes = [];
              await this.cargarHistorialChats();
            }

            const userMsg = { texto: this.nuevoMensaje, tipo: "usuario" };
            this.mensajes.push(userMsg);
            
            const response = await chatService.sendMessage(
              this.nuevoMensaje,
              this.chat_id
            );
            
            this.mensajes.push({ 
              texto: response.respuesta, 
              tipo: "ia" 
            });
            
            this.nuevoMensaje = '';
            this.scrollToBottom();
          } catch (error) {
            console.error("Error al enviar mensaje:", error);
            alert("Error al enviar el mensaje");
          } finally {
            this.enviando = false;
          }
        },

        async nuevoChat() {
          try {
            const res = await chatService.createNewChat();
            this.chat_id = res.id_chat;
            this.chatSeleccionado = res.id_chat;
            this.mensajes = [];
            await this.cargarHistorialChats();
          } catch (e) { console.error(e) }
        },

        async Ayuda() {
          try {
            if (!this.chat_id) {
              alert("Primero debes iniciar o seleccionar un chat.");
              return;
            }

            await chatService.help(this.chat_id);
            alert("Solicitud de ayuda enviada correctamente.");
          } catch (error) {
            console.error("Error al solicitar ayuda:", error);
            alert("Ocurrió un error al enviar la solicitud de ayuda.");
          }
        },

        scrollToBottom() {
          this.$nextTick(() => {
            const chatContainer = document.getElementById("chat-mensajes");
            if (chatContainer) {
              chatContainer.scrollTop = chatContainer.scrollHeight;
            }
          });
        },
        	
        adminInterfaz(){
          window.location.href = "VentanaAdmin.html";
        },
        cerrarSesion() {

          // Si es invitado, eliminar usuario.
          if (this.esInvitado) {
            authService.delete()
              .then(() => {
                console.log("Usuario invitado eliminado");
                authService.logout();
                window.location.href = "index.html";
              });
          } else {
            authService.logout();
            window.location.href = "index.html";
          }
        }
      },
      mounted() {
        this.cargarHistorialChats();
      }

    });
    
    this.app.mount('#app');
  }
}