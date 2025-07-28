<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Catálogo de servicios</h1>
    
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
              @input="handleSearch"
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
        <select v-model="selectedCategory" class="select select-bordered w-full" @change="handleCategoryChange">
          <option value="">Todas las categorías</option>
          <option v-for="category in categories" :key="category.id" :value="category.slug">
            {{ category.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-16">
      <span class="loading loading-spinner loading-lg"></span>
      <p class="text-gray-600 mt-2">Cargando servicios...</p>
    </div>

    <!-- Services Grid -->
    <div v-else-if="services.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="service in services" :key="service.id" class="card bg-base-100 shadow-xl card-hover">
        <figure v-if="service.image" class="px-10 pt-10">
          <img :src="service.image" :alt="service.name" class="rounded-lg h-32 w-full object-cover" />
        </figure>
        <figure v-else class="px-10 pt-10">
          <div class="w-20 h-20 bg-primary-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </figure>
        <div class="card-body items-center text-center">
          <h2 class="card-title">{{ service.name }}</h2>
          <p>{{ service.short_description || service.description }}</p>
          <div class="badge badge-secondary">{{ service.category_name }}</div>
          <div class="text-sm font-semibold text-primary mt-2">{{ service.price_display }}</div>
          <div class="card-actions mt-4">
            <button @click="openServiceModal(service)" class="btn btn-primary btn-sm">Ver detalles</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No se encontraron servicios</h3>
      <p class="text-gray-600">Intenta con otros términos de búsqueda o categorías</p>
    </div>

    <!-- Service Detail Modal -->
    <div v-if="selectedService" class="modal modal-open" @click="closeModal">
      <div class="modal-box max-w-3xl" @click.stop>
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeModal">✕</button>
        
        <h3 class="font-bold text-2xl mb-4">{{ selectedService.name }}</h3>
        
        <div v-if="selectedService.image" class="mb-6">
          <img :src="selectedService.image" :alt="selectedService.name" class="w-full h-64 object-cover rounded-lg" />
        </div>
        
        <div class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Descripción</p>
            <p class="text-gray-700">{{ selectedService.description }}</p>
          </div>
          
          <div v-if="selectedService.features_list && selectedService.features_list.length > 0">
            <p class="text-sm text-gray-500 mb-2">Características</p>
            <ul class="list-disc list-inside space-y-1">
              <li v-for="(feature, index) in selectedService.features_list" :key="index">
                {{ feature }}
              </li>
            </ul>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-if="selectedService.duration">
              <p class="text-sm text-gray-500">Duración</p>
              <p class="font-semibold">{{ selectedService.duration }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Precio</p>
              <p class="font-semibold text-primary">{{ selectedService.price_display }}</p>
            </div>
          </div>
          
          <div v-if="selectedService.provider_name" class="border-t pt-4">
            <p class="text-sm text-gray-500 mb-2">Proveedor</p>
            <p class="font-semibold">{{ selectedService.provider_name }}</p>
            <div class="flex gap-4 mt-2">
              <a v-if="selectedService.provider_email" :href="`mailto:${selectedService.provider_email}`" class="link link-primary text-sm">
                {{ selectedService.provider_email }}
              </a>
              <a v-if="selectedService.provider_phone" :href="`tel:${selectedService.provider_phone}`" class="link link-primary text-sm">
                {{ selectedService.provider_phone }}
              </a>
            </div>
            <a v-if="selectedService.provider_website" :href="selectedService.provider_website" target="_blank" class="link link-primary text-sm">
              {{ selectedService.provider_website }}
            </a>
          </div>
        </div>

        <div class="modal-action">
          <router-link :to="{ name: 'Contacto' }" class="btn btn-primary">
            Solicitar información
          </router-link>
          <button class="btn" @click="closeModal">Cerrar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()

// State
const searchQuery = ref('')
const selectedCategory = ref('')
const loading = ref(false)
const services = ref([])
const categories = ref([])
const selectedService = ref(null)


// Fetch categories
const fetchCategories = async () => {
  try {
    const response = await api.get('/oferta/categories/')
    categories.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

// Fetch services
const fetchServices = async () => {
  loading.value = true
  try {
    const params = {
      search: searchQuery.value,
      category: selectedCategory.value,
      ordering: '-is_featured,order,name'
    }
    
    const response = await api.get('/oferta/services/', { params })
    services.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching services:', error)
    toast.error('Error al cargar los servicios')
  } finally {
    loading.value = false
  }
}

// Handle search
const handleSearch = () => {
  fetchServices()
}

// Handle category change
const handleCategoryChange = () => {
  fetchServices()
}

// Open service detail modal
const openServiceModal = async (service) => {
  try {
    const response = await api.get(`/oferta/services/${service.slug}/`)
    selectedService.value = response.data
  } catch (error) {
    console.error('Error fetching service details:', error)
    selectedService.value = service
  }
}

// Close modal
const closeModal = () => {
  selectedService.value = null
}


// Watch for search query changes with debounce
let searchTimeout = null
watch(searchQuery, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchServices()
  }, 500)
})

// Initialize
onMounted(() => {
  fetchCategories()
  fetchServices()
})
</script>