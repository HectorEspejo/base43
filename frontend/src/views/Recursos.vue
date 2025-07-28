<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary/10 to-secondary/10 py-12">
      <div class="container-custom mx-auto section-padding">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Mapa de Recursos</h1>
        <p class="text-lg text-gray-700 max-w-3xl">
          Explora instituciones, organizaciones y recursos disponibles en tu área. 
          Encuentra apoyo, servicios y oportunidades para proyectos de vivienda colaborativa.
        </p>
      </div>
    </section>

    <!-- Main Content -->
    <section class="container-custom mx-auto section-padding py-8">
      <!-- Tabs -->
      <div class="tabs tabs-boxed mb-8">
        <a 
          class="tab" 
          :class="{ 'tab-active': activeTab === 'map' }"
          @click="activeTab = 'map'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Vista Mapa
        </a>
        <a 
          class="tab"
          :class="{ 'tab-active': activeTab === 'table' }"
          @click="activeTab = 'table'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          Vista Tabla
        </a>
      </div>

      <!-- Map View -->
      <div v-if="activeTab === 'map'" class="space-y-6">
        <!-- Map Container -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body p-0">
            <div id="map" class="w-full h-[600px] rounded-lg bg-gray-200 overflow-hidden">
              <!-- Google Maps Embed -->
              <iframe 
                src="https://www.google.com/maps/d/embed?mid=1SKv5u5IFGzWewloqYcPXVW43ky4pido&ehbc=2E312F&noprof=1" 
                width="100%" 
                height="100%"
                style="border:0;"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
      </div>

      <!-- Table View -->
      <div v-else class="space-y-6">
        <!-- Search and Filters -->
        <div class="flex flex-col lg:flex-row gap-4">
          <div class="form-control flex-1">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Buscar recursos..." 
              class="input input-bordered w-full"
              @input="handleSearch"
            />
          </div>
          <select v-model="filterType" class="select select-bordered" @change="filterResources">
            <option value="">Todos los tipos</option>
            <option v-for="type in types" :key="type.code" :value="type.code">
              {{ type.name }} ({{ type.count }})
            </option>
          </select>
          <select v-model="filterCity" class="select select-bordered" @change="filterResources">
            <option value="">Todas las ciudades</option>
            <option v-for="city in cities" :key="city.code" :value="city.code">
              {{ city.name }} ({{ city.count }})
            </option>
          </select>
        </div>

        <!-- Resources Table -->
        <div class="overflow-x-auto">
          <table class="table table-zebra w-full">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Dirección</th>
                <th>Ciudad</th>
                <th>Teléfono</th>
                <th>Email</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="resource in paginatedResources" :key="resource.id">
                <td>
                  <div>
                    <div class="font-bold">{{ resource.name }}</div>
                    <div class="text-sm opacity-70">{{ resource.category_name }}</div>
                  </div>
                </td>
                <td>
                  <span class="badge badge-sm" :class="getTypeBadgeClass(resource.type)">
                    {{ resource.type_display || resource.type }}
                  </span>
                </td>
                <td>{{ resource.address }}</td>
                <td>{{ resource.city_display || resource.city }}</td>
                <td>{{ resource.phone || '-' }}</td>
                <td>{{ resource.email || '-' }}</td>
                <td>
                  <div class="flex gap-2">
                    <button 
                      @click="viewDetails(resource)"
                      class="btn btn-ghost btn-xs"
                      title="Ver detalles"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button 
                      @click="showOnMap(resource)"
                      class="btn btn-ghost btn-xs"
                      title="Ver en mapa"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Loading state -->
          <div v-if="loading" class="text-center py-8">
            <span class="loading loading-spinner loading-lg"></span>
            <p class="text-gray-500 mt-2">Cargando recursos...</p>
          </div>
          
          <!-- No results message -->
          <div v-else-if="filteredResources.length === 0" class="text-center py-8">
            <p class="text-gray-500">No se encontraron recursos con los filtros actuales</p>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex justify-center">
          <div class="btn-group">
            <button 
              class="btn btn-sm"
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
            >
              «
            </button>
            <button 
              v-for="page in displayedPages" 
              :key="page"
              class="btn btn-sm"
              :class="{ 'btn-active': page === currentPage }"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            <button 
              class="btn btn-sm"
              :disabled="currentPage === totalPages"
              @click="changePage(currentPage + 1)"
            >
              »
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Resource Details Modal -->
    <div v-if="selectedResource" class="modal modal-open" @click="closeModal">
      <div class="modal-box max-w-3xl" @click.stop>
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeModal">✕</button>
        
        <h3 class="font-bold text-2xl mb-4">{{ selectedResource.name }}</h3>
        
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Tipo</p>
              <p class="font-semibold">{{ selectedResource.type_display || selectedResource.type }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Categoría</p>
              <p class="font-semibold">{{ selectedResource.category?.name || selectedResource.category_name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Dirección</p>
              <p class="font-semibold">{{ selectedResource.full_address || `${selectedResource.address}, ${selectedResource.city_display || selectedResource.city}` }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Teléfono</p>
              <p class="font-semibold">{{ selectedResource.phone || 'No disponible' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Email</p>
              <p class="font-semibold">{{ selectedResource.email || 'No disponible' }}</p>
            </div>
            <div v-if="selectedResource.website">
              <p class="text-sm text-gray-500">Sitio web</p>
              <a :href="selectedResource.website" target="_blank" class="link link-primary">
                {{ selectedResource.website }}
              </a>
            </div>
          </div>
          
          <div>
            <p class="text-sm text-gray-500 mb-2">Descripción</p>
            <p class="text-gray-700">{{ selectedResource.description }}</p>
          </div>

          <div v-if="selectedResource.services_list && selectedResource.services_list.length > 0">
            <p class="text-sm text-gray-500 mb-2">Servicios ofrecidos</p>
            <div class="flex flex-wrap gap-2">
              <span v-for="service in selectedResource.services_list" :key="service" class="badge badge-outline">
                {{ service }}
              </span>
            </div>
          </div>

          <div v-if="selectedResource.schedule">
            <p class="text-sm text-gray-500 mb-2">Horario</p>
            <p class="text-gray-700">{{ selectedResource.schedule }}</p>
          </div>
        </div>

        <div class="modal-action">
          <button class="btn btn-primary" @click="showOnMap(selectedResource)">
            Ver en mapa
          </button>
          <button class="btn" @click="closeModal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()

// State
const activeTab = ref('map')
const searchQuery = ref('')
const filterType = ref('')
const filterCity = ref('')
const selectedCategories = ref([])
const selectedResource = ref(null)
const currentPage = ref(1)
const itemsPerPage = 10
const loading = ref(false)
const cities = ref([])
const types = ref([])
const totalCount = ref(0)

// Data from API
const categories = ref([])
const resources = ref([])

// Computed
const filteredResources = computed(() => {
  let filtered = resources.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(resource => 
      resource.name.toLowerCase().includes(query) ||
      resource.description.toLowerCase().includes(query) ||
      (resource.category_name || '').toLowerCase().includes(query)
    )
  }

  // Type filter
  if (filterType.value) {
    filtered = filtered.filter(resource => resource.type === filterType.value)
  }

  // City filter
  if (filterCity.value) {
    filtered = filtered.filter(resource => resource.city === filterCity.value)
  }

  // Category filter (for map view)
  if (selectedCategories.value.length > 0) {
    filtered = filtered.filter(resource => 
      selectedCategories.value.includes(resource.category)
    )
  }

  return filtered
})

const paginatedResources = computed(() => {
  // If using backend pagination, return resources directly
  if (totalCount.value > 0) {
    return resources.value
  }
  // Otherwise use local pagination
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredResources.value.slice(start, end)
})

const totalPages = computed(() => {
  // If using backend pagination, calculate from totalCount
  if (totalCount.value > 0) {
    return Math.ceil(totalCount.value / 20) // Backend PAGE_SIZE is 20
  }
  // Otherwise use local pagination
  return Math.ceil(filteredResources.value.length / itemsPerPage)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPages = 5
  const halfPages = Math.floor(maxPages / 2)
  
  let start = Math.max(1, currentPage.value - halfPages)
  let end = Math.min(totalPages.value, start + maxPages - 1)
  
  if (end - start + 1 < maxPages) {
    start = Math.max(1, end - maxPages + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// API Methods
const fetchCategories = async () => {
  try {
    const response = await api.get('/recursos/categories/')
    // Handle paginated response
    const data = response.data.results || response.data
    categories.value = Array.isArray(data) ? data.map(cat => ({
      ...cat,
      count: cat.resource_count
    })) : []
  } catch (error) {
    console.error('Error fetching categories:', error)
    toast.error('Error al cargar las categorías')
  }
}

const fetchResources = async () => {
  loading.value = true
  try {
    const params = {
      search: searchQuery.value,
      type: filterType.value,
      city: filterCity.value,
      ordering: '-is_featured,name',
      page: currentPage.value
    }
    
    const response = await api.get('/recursos/', { params })
    // Handle paginated response
    if (response.data.results) {
      resources.value = response.data.results
      totalCount.value = response.data.count || 0
    } else {
      resources.value = Array.isArray(response.data) ? response.data : []
      totalCount.value = resources.value.length
    }
  } catch (error) {
    console.error('Error fetching resources:', error)
    toast.error('Error al cargar los recursos')
    resources.value = []
    totalCount.value = 0
  } finally {
    loading.value = false
  }
}

const fetchCities = async () => {
  try {
    const response = await api.get('/recursos/cities/')
    cities.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error('Error fetching cities:', error)
    cities.value = []
  }
}

const fetchTypes = async () => {
  try {
    const response = await api.get('/recursos/types/')
    types.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error('Error fetching types:', error)
    types.value = []
  }
}

// Methods
const handleSearch = () => {
  currentPage.value = 1
  fetchResources()
}

const filterResources = () => {
  currentPage.value = 1
  fetchResources()
}

const viewDetails = async (resource) => {
  try {
    // Fetch full details from API
    const response = await api.get(`/recursos/${resource.id}/`)
    selectedResource.value = response.data
  } catch (error) {
    console.error('Error fetching resource details:', error)
    toast.error('Error al cargar los detalles del recurso')
    // Fallback to basic data
    selectedResource.value = resource
  }
}

const showOnMap = (resource) => {
  activeTab.value = 'map'
  // In the future, this will center the map on the resource
  toast.info(`Mostrando ${resource.name} en el mapa`)
  closeModal()
}

const closeModal = () => {
  selectedResource.value = null
}

const changePage = (page) => {
  currentPage.value = page
  fetchResources()
}

const getTypeBadgeClass = (type) => {
  const classes = {
    institucion: 'badge-primary',
    organizacion: 'badge-secondary',
    servicio: 'badge-accent',
    programa: 'badge-info',
    cooperativa: 'badge-warning',
    empresa: 'badge-success'
  }
  return classes[type] || 'badge-ghost'
}

// Initialize data when component mounts
onMounted(async () => {
  // Load initial data
  await Promise.all([
    fetchCategories(),
    fetchResources(),
    fetchCities(),
    fetchTypes()
  ])
  
  // Google Maps initialization will go here when ready
  console.log('Recursos component mounted - Map initialization pending')
})
</script>

<style scoped>
/* Custom styles for the map */
#map {
  min-height: 600px;
}

@media (max-width: 768px) {
  #map {
    min-height: 400px;
  }
}
</style>