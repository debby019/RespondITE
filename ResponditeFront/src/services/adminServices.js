// src/services/adminServices.js
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

const supabase = createClient(
  'https://nulsoiwjscvaxzxyjfgm.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51bHNvaXdqc2N2YXh6eHlqZmdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI0NDgzMzcsImV4cCI6MjA1ODAyNDMzN30.WeWkC1Migmn8QKYI3XjvQ0CEnHo4eizH5_XImTvHfzw' // Tu clave pública
);

export async function fetchProcesosYConsultas() {
  const { data: procesos, error: errorProcesos } = await supabase.from('procesos').select('*');
  if (errorProcesos) throw errorProcesos;

  const { data: conocimiento, error: errorConocimiento } = await supabase.from('base_conocimiento').select('*');
  if (errorConocimiento) throw errorConocimiento;

  return procesos.map(p => ({
    ...p,
    consultas: conocimiento.filter(c => c.proceso_id === p.id_proceso),
  }));
}

export async function agregarProceso(nombre, consultas) {
  const { data, error } = await supabase.from('procesos').insert({ nombre }).select();
  if (error || !data.length) throw error;
  const newProcesoId = data[0].id_proceso;

  for (const c of consultas) {
    await supabase.from('base_conocimiento').insert({
      proceso_id: newProcesoId,
      consulta: c.consulta,
      informacion: c.informacion,
    });
  }
}

export async function actualizarProceso(id, nombre, consultas) {
  await supabase.from('procesos').update({ nombre }).eq('id_proceso', id);
  await supabase.from('base_conocimiento').delete().eq('proceso_id', id);
  for (const c of consultas) {
    await supabase.from('base_conocimiento').insert({
      proceso_id: id,
      consulta: c.consulta,
      informacion: c.informacion,
    });
  }
}

export async function eliminarProceso(id) {
  await supabase.from('base_conocimiento').delete().eq('proceso_id', id);
  await supabase.from('procesos').delete().eq('id_proceso', id);
}
