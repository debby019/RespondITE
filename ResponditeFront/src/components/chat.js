import { chatService } from '../services/chatServices.js';
import { authService } from '../services/authServices.js';
import { validateSession } from '../services/sessionValidator.js';

window.addEventListener("DOMContentLoaded", () => {
  const userData = validateSession();

  if (!userData) return;

  const { usuario_id, role, chat_id } = userData;

  new ChatInterface();  
});

export class ChatInterface {
  constructor() {
    if (!authService.isAuthenticated()) {
      window.location.href = "index.html";
      return;
    }

    this.currentUser = authService.getCurrentUser();

    if (!this.currentUser?.id) {
      authService.logout();
      window.location.href = "index.html";
      return;
    } 

    const vueData = {
      fecha: new Date().toLocaleDateString('es-MX', { 
        day: '2-digit', 
        month: 'long', 
        year: 'numeric' 
      }),
      nuevoMensaje: '',
      mensajes: [],
      chats: [],
      chatSeleccionado: null,
      chat_id: null, 
      enviando: false,
      usuario_id: this.currentUser.id,
      esAdmin: this.currentUser.role === 'admin',
    };

    this.initVueApp(vueData);
  }

  initVueApp(initialData) {
    this.app = Vue.createApp({
      data() {
        return initialData; 
      },
      methods: {
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

        async enviarMensaje() {
          if (!this.nuevoMensaje.trim() || this.enviando) return;

          try {
            this.enviando = true;
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
          authService.logout();
          window.location.href = "index.html";
        }
      },
      mounted() {
        this.cargarHistorialChats();
        this.nuevoChat();
      }

    });
    
    this.app.mount('#app');
  }
}