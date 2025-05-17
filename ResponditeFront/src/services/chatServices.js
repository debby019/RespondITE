import { api } from './api.js';

export const chatService = {
  async sendMessage(mensaje, chatId) {
    return api.post("/chat", {
      user_input: mensaje,
      chat_id: chatId,
      tone: "neutral"
    });
  },

  async getChatHistory(chatId) {
    return api.get(`/chats/${chatId}/mensajes`);
  },

  async createNewChat() {
    return api.post("/chats/nuevo");
  },

  
  async getUserChats() {
    const user = JSON.parse(localStorage.getItem('user'));
    return api.post('/chats', { usuario_id: user.id }); 
  },

  async help(chatId) {
    return api.post("/chats/help", { chat_id: chatId });
  }


};


