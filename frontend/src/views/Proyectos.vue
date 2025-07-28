<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Proyectos de Vivienda</h1>
    
    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-8">
      <button 
        v-for="category in categories" 
        :key="category.slug"
        @click="selectedType = category.slug"
        class="btn btn-sm"
        :class="selectedType === category.slug ? 'btn-primary' : 'btn-outline'"
      >
        {{ category.name }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-16">
      <span class="loading loading-spinner loading-lg"></span>
      <p class="text-gray-600 mt-2">Cargando proyectos...</p>
    </div>

    <!-- Projects Grid -->
    <div v-else-if="projects.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="project in filteredProjects" 
        :key="project.id" 
        class="card bg-base-100 shadow-xl card-hover"
      >
        <figure>
          <img 
            :src="project.image || 'https://placehold.co/600x400'" 
            :alt="project.name"
            class="h-48 w-full object-cover"
          />
        </figure>
        <div class="card-body">
          <h2 class="card-title">
            {{ project.name }}
            <div class="badge badge-secondary">{{ project.category_name }}</div>
          </h2>
          <p class="text-sm text-gray-600">{{ project.location }}</p>
          <p>{{ project.short_description }}</p>
          
          <div class="flex items-center gap-4 mt-4 text-sm">
            <div class="flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span>{{ project.participants }} participantes</span>
            </div>
            <div class="flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span>{{ project.units }} unidades</span>
            </div>
          </div>
          
          <div class="card-actions justify-between items-center mt-4">
            <div class="badge" :class="getStatusBadgeClass(project.status)">
              {{ project.status_display }}
            </div>
            <button @click="openProjectModal(project)" class="btn btn-primary btn-sm">Ver más</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No se encontraron proyectos</h3>
      <p class="text-gray-600">No hay proyectos que coincidan con los filtros seleccionados</p>
    </div>

    <!-- Project Detail Modal -->
    <div v-if="selectedProject" class="modal modal-open" @click="closeModal">
      <div class="modal-box max-w-4xl" @click.stop>
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeModal">✕</button>
        
        <div v-if="selectedProject.image" class="mb-6">
          <img :src="selectedProject.image" :alt="selectedProject.name" class="w-full h-64 object-cover rounded-lg" />
        </div>
        
        <h3 class="font-bold text-2xl mb-2">{{ selectedProject.name }}</h3>
        <div class="flex items-center gap-2 mb-4">
          <div class="badge badge-secondary">{{ selectedProject.category.name }}</div>
          <div class="badge" :class="getStatusBadgeClass(selectedProject.status)">
            {{ selectedProject.status_display }}
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-semibold mb-2">Información general</h4>
            <div class="space-y-2 text-sm">
              <p><span class="font-medium">Ubicación:</span> {{ selectedProject.location }}</p>
              <p v-if="selectedProject.address"><span class="font-medium">Dirección:</span> {{ selectedProject.address }}</p>
              <p><span class="font-medium">Unidades:</span> {{ selectedProject.units }}</p>
              <p><span class="font-medium">Participantes:</span> {{ selectedProject.participants }}</p>
              <p v-if="selectedProject.start_date"><span class="font-medium">Fecha de inicio:</span> {{ new Date(selectedProject.start_date).toLocaleDateString() }}</p>
              <p v-if="selectedProject.estimated_completion"><span class="font-medium">Finalización estimada:</span> {{ new Date(selectedProject.estimated_completion).toLocaleDateString() }}</p>
            </div>
          </div>
          
          <div v-if="selectedProject.features_list && selectedProject.features_list.length > 0">
            <h4 class="font-semibold mb-2">Características</h4>
            <ul class="list-disc list-inside space-y-1 text-sm">
              <li v-for="(feature, index) in selectedProject.features_list" :key="index">
                {{ feature }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="mt-6">
          <h4 class="font-semibold mb-2">Descripción</h4>
          <p class="text-gray-700" v-if="selectedProject.description">{{ selectedProject.description }}</p>
          <p class="text-gray-500 italic" v-else>No hay descripción disponible</p>
        </div>
        
        <div v-if="selectedProject.investment_range" class="mt-4">
          <p class="text-sm"><span class="font-medium">Rango de inversión:</span> {{ selectedProject.investment_range }}</p>
        </div>
        
        <div v-if="selectedProject.financing_type" class="mt-2">
          <p class="text-sm"><span class="font-medium">Tipo de financiación:</span> {{ selectedProject.financing_type }}</p>
        </div>
        
        <div v-if="selectedProject.updates && selectedProject.updates.length > 0" class="mt-6">
          <h4 class="font-semibold mb-2">Últimas actualizaciones</h4>
          <div class="space-y-2">
            <div v-for="update in selectedProject.updates" :key="update.id" class="border-l-2 border-primary pl-4">
              <h5 class="font-medium">{{ update.title }}</h5>
              <p class="text-sm text-gray-600">{{ update.content }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ new Date(update.created_at).toLocaleDateString() }}</p>
            </div>
          </div>
        </div>
        
        <div class="modal-action">
          <a v-if="selectedProject.website" :href="selectedProject.website" target="_blank" class="btn btn-primary">
            Visitar sitio web
          </a>
          <router-link :to="{ name: 'Contacto' }" class="btn btn-secondary">
            Solicitar información
          </router-link>
          <button class="btn" @click="closeModal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()

// State
const selectedType = ref('todos')
const loading = ref(false)
const projects = ref([])
const categories = ref([])
const selectedProject = ref(null)

// Fetch categories
const fetchCategories = async () => {
  try {
    const response = await api.get('/proyectos/categories/')
    const data = response.data.results || response.data
    categories.value = [
      { slug: 'todos', name: 'Todos' },
      ...data
    ]
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

// Fetch projects
const fetchProjects = async () => {
  loading.value = true
  try {
    const params = {
      ordering: '-is_featured,order,-created_at'
    }
    
    if (selectedType.value !== 'todos') {
      params.category = selectedType.value
    }
    
    const response = await api.get('/proyectos/projects/', { params })
    projects.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching projects:', error)
    toast.error('Error al cargar los proyectos')
  } finally {
    loading.value = false
  }
}

// Get project details
const getProjectDetails = async (project) => {
  if (!project || !project.slug) {
    console.error('Invalid project:', project)
    toast.error('Proyecto inválido')
    return
  }
  
  try {
    const response = await api.get(`/proyectos/projects/${project.slug}/`)
    selectedProject.value = response.data
  } catch (error) {
    console.error('Error fetching project details:', error)
    if (error.response) {
      console.error('Error status:', error.response.status)
      console.error('Error data:', error.response.data)
    }
    toast.error('Error al cargar los detalles del proyecto')
    selectedProject.value = null
  }
}

// Open project modal
const openProjectModal = (project) => {
  getProjectDetails(project)
}

// Close modal
const closeModal = () => {
  selectedProject.value = null
}

// Computed
const filteredProjects = computed(() => projects.value)

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'planning': 'badge-secondary',
    'development': 'badge-info', 
    'construction': 'badge-warning',
    'active': 'badge-success',
    'completed': 'badge-primary',
    'paused': 'badge-ghost'
  }
  return statusClasses[status] || 'badge-ghost'
}

// Watch for category changes
watch(selectedType, () => {
  fetchProjects()
})

// Initialize
onMounted(() => {
  fetchCategories()
  fetchProjects()
})
</script>