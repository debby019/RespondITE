import { api } from './api.js';

export async function fetchProcesos() {
  const resp = await api.get('/admin/procesos');
  console.log("Procesos cargados:", resp);
  return resp;
}

export async function createProceso(form) {
  return api.post('/admin/procesos', form);
}

export async function updateProceso(id, form) {
  return api.put(`/admin/procesos/${id}`, form);
}

export async function deleteProcesoYConsultas(id) {
  return api.delete(`/admin/procesos/${id}`);
}