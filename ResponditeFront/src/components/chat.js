import { chatService } from '../services/chatServices.js';
import { authService } from '../services/authServices.js';

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
      enviando: false,
      usuario_id: this.currentUser.id,
      chat_id: this.currentUser.chat_id
    };

    this.initVueApp(vueData);
  }

  initVueApp(initialData) {
    this.app = Vue.createApp({
      data() {
        return initialData; 
      },
      methods: {
        async cargarMensajes() {
          try {
            const mensajes = await chatService.getChatHistory(this.chat_id);
            this.mensajes = mensajes.map(msg => ({
              texto: msg.contenido || msg.Mensaje,
              tipo: msg.remitente === 'usuario' ? 'usuario' : 'ia',
              timestamp: msg.timestamp
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

        scrollToBottom() {
          this.$nextTick(() => {
            const chatContainer = document.getElementById("chat-mensajes");
            if (chatContainer) {
              chatContainer.scrollTop = chatContainer.scrollHeight;
            }
          });
        }
      },
      mounted() {
        this.cargarMensajes();
      }
    });

    this.app.mount('#app');
  }
}