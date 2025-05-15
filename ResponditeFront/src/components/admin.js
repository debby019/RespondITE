// src/components/admin.js
import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import {
  fetchProcesosYConsultas,
  agregarProceso,
  actualizarProceso,
  eliminarProceso
} from '../services/adminServices.js';
import { validateSession } from '../services/sessionValidator.js';

createApp({
  data() {
    return {
      procesos: [],
      form: {
        nombre: '',
        consultas: [{ consulta: '', informacion: '' }]
      },
      currentEditIndex: null
    };
  },
  computed: {
    isEditing() {
      return this.currentEditIndex !== null;
    }
  },
  methods: {
    async cargarProcesos() {
      try {
        this.procesos = await fetchProcesosYConsultas();
        console.log('Procesos cargados:', this.procesos);
      } catch (err) {
        console.error('Error al cargar procesos:', err);
      }
    },
    openModal() {
      this.form = {
        nombre: '',
        consultas: [{ consulta: '', informacion: '' }]
      };
      this.currentEditIndex = null;
      new bootstrap.Modal(document.getElementById('processModal')).show();
    },
    editProceso(index) {
      const p = this.procesos[index];
      this.form = {
        nombre: p.nombre,
        consultas: p.consultas.map(c => ({
          consulta: c.consulta,
          informacion: c.informacion
        }))
      };
      this.currentEditIndex = index;
      new bootstrap.Modal(document.getElementById('processModal')).show();
    },
    async saveProceso() {
      try {
        if (this.isEditing) {
          const id = this.procesos[this.currentEditIndex].id_proceso;
          await actualizarProceso(id, this.form.nombre, this.form.consultas);
        } else {
          await agregarProceso(this.form.nombre, this.form.consultas);
        }
        bootstrap.Modal.getInstance(document.getElementById('processModal')).hide();
        await this.cargarProcesos();
      } catch (err) {
        console.error('Error al guardar proceso:', err);
        alert('Error al guardar proceso');
      }
    },
    async deleteProceso(index) {
      try {
        const id = this.procesos[index].id_proceso;
        await eliminarProceso(id);
        await this.cargarProcesos();
      } catch (err) {
        console.error('Error al eliminar proceso:', err);
        alert('Error al eliminar proceso');
      }
    },
    addConsulta() {
      this.form.consultas.push({ consulta: '', informacion: '' });
    },
    removeConsulta(index) {
      this.form.consultas.splice(index, 1);
    }
  },
  async mounted() {
    const userData = validateSession();
    if (!userData || userData.role !== 'admin') {
      console.warn('Acceso denegado. Redirigiendo...');
      window.location.href = 'index.html';
    } else {
      console.log('Usuario autenticado:', userData);
      await this.cargarProcesos();
    }
  }
}).mount('#app');
