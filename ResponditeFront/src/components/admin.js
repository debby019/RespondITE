import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
import {
  fetchProcesos,
  updateProceso,
  createProceso,
  deleteProcesoYConsultas
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
        this.procesos = await fetchProcesos();
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
          await updateProceso(id, {
            nombre: this.form.nombre,
            consultas: this.form.consultas
          });
        } else {
          await createProceso({
            nombre: this.form.nombre,
            consultas: this.form.consultas
          });

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
        await deleteProcesoYConsultas(id);
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
    },
    logout() {
      authService.logout();
      window.location.href = "index.html";
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
      document.body.classList.add('loaded');

    }
  }
}).mount('#app');