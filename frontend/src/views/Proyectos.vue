<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Proyectos de Vivienda</h1>
    
    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-8">
      <button 
        v-for="type in projectTypes" 
        :key="type.value"
        @click="selectedType = type.value"
        class="btn btn-sm"
        :class="selectedType === type.value ? 'btn-primary' : 'btn-outline'"
      >
        {{ type.label }}
      </button>
    </div>

    <!-- Projects Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
            <div class="badge badge-secondary">{{ project.type }}</div>
          </h2>
          <p class="text-sm text-gray-600">{{ project.location }}</p>
          <p>{{ project.description }}</p>
          
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
              {{ project.status }}
            </div>
            <button class="btn btn-primary btn-sm">Ver más</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredProjects.length === 0" class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No se encontraron proyectos</h3>
      <p class="text-gray-600">No hay proyectos que coincidan con los filtros seleccionados</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedType = ref('todos')

const projectTypes = [
  { value: 'todos', label: 'Todos' },
  { value: 'cohousing', label: 'Cohousing' },
  { value: 'cooperativa', label: 'Cooperativas' },
  { value: 'menores', label: 'Centros de menores' },
  { value: 'social', label: 'Vivienda social' }
]

// Mock data - replace with API call
const projects = ref([
  {
    id: 1,
    name: 'Centro de protección de menores en suelo público',
    type: 'menores',
    location: 'Málaga, Andalucía',
    description: 'Proyecto para la puesta en marcha de un centro de menores.',
    participants: 3,
    units: 25,
    status: 'En desarrollo',
    image: null
  },
  {
    id: 2,
    name: 'Cooperativa de vivienda en cesión de uso',
    type: 'cooperativa',
    location: 'Málaga, Andalucía',
    description: 'Cooperativa de vivienda en cesión de uso con criterios de sostenibilidad y eficiencia energética.',
    participants: 32,
    units: 20,
    status: 'En desarrollo',
    image: null
  }
])

const filteredProjects = computed(() => {
  if (selectedType.value === 'todos') return projects.value
  return projects.value.filter(project => project.type === selectedType.value)
})

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'Activo': 'badge-success',
    'En construcción': 'badge-warning',
    'En desarrollo': 'badge-info',
    'Planificación': 'badge-secondary'
  }
  return statusClasses[status] || 'badge-ghost'
}
</script>