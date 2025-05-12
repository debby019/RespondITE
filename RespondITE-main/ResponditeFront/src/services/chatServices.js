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

  async createNewChat(usuarioId) {
    return api.post("/chats/nuevo", { usuario_id: usuarioId });
  }
};