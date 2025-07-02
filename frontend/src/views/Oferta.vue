<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Catálogo de Servicios</h1>
    
    <!-- Search and Filters -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
      <div class="lg:col-span-3">
        <div class="form-control">
          <div class="input-group">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar servicios..." 
              class="input input-bordered w-full"
            />
            <button class="btn btn-square btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <div>
        <select v-model="selectedCategory" class="select select-bordered w-full">
          <option value="">Todas las categorías</option>
          <option value="arquitectura">Arquitectura</option>
          <option value="construccion">Construcción</option>
          <option value="legal">Legal</option>
          <option value="financiero">Financiero</option>
          <option value="consultoria">Consultoría</option>
        </select>
      </div>
    </div>

    <!-- Services Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="service in filteredServices" :key="service.id" class="card bg-base-100 shadow-xl card-hover">
        <figure class="px-10 pt-10">
          <div class="w-20 h-20 bg-primary-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </figure>
        <div class="card-body items-center text-center">
          <h2 class="card-title">{{ service.name }}</h2>
          <p>{{ service.description }}</p>
          <div class="badge badge-secondary">{{ service.category }}</div>
          <div class="card-actions mt-4">
            <button @click="openServiceModal(service)" class="btn btn-primary btn-sm">Ver detalles</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredServices.length === 0" class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No se encontraron servicios</h3>
      <p class="text-gray-600">Intenta con otros términos de búsqueda o categorías</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategory = ref('')

// Mock data - replace with API call
const services = ref([
  {
    id: 1,
    name: 'Arquitectura Sostenible',
    description: 'Diseño de viviendas ecológicas y eficientes',
    category: 'arquitectura',
    provider: 'EcoArquitectos'
  },
  {
    id: 2,
    name: 'Construcción Modular',
    description: 'Sistemas de construcción prefabricada y modular',
    category: 'construccion',
    provider: 'ModuHomes'
  },
  {
    id: 3,
    name: 'Asesoría Legal Cooperativas',
    description: 'Asesoramiento legal para cooperativas de vivienda',
    category: 'legal',
    provider: 'Abogados Asociados'
  },
  // Add more services...
])

const filteredServices = computed(() => {
  return services.value.filter(service => {
    const matchesSearch = service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = !selectedCategory.value || service.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const openServiceModal = (service) => {
  // TODO: Implement modal or navigate to detail page
  console.log('Opening service:', service)
}
</script>