<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Repositorio de Documentos</h1>
    
    <!-- Categories View -->
    <div v-if="!selectedCategory" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="category in categories" :key="category.id">
        <div 
          @click="selectCategory(category)"
          class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow cursor-pointer"
        >
          <div class="card-body items-center text-center">
            <div class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
            </div>
            <h2 class="card-title">{{ category.name }}</h2>
            <p class="text-gray-600">{{ category.description }}</p>
            <div class="text-sm text-gray-500 mt-2">
              <span v-if="category.directories_count">{{ category.directories_count }} carpetas</span>
              <span v-if="category.directories_count && category.files_count" class="mx-1">•</span>
              <span v-if="category.files_count">{{ category.files_count }} archivos</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Files Browser View -->
    <div v-else>
      <!-- Breadcrumb -->
      <div class="text-sm breadcrumbs mb-6">
        <ul>
          <li><a @click="resetView" class="cursor-pointer">Inicio</a></li>
          <li v-if="selectedCategory">
            <a @click="selectCategory(selectedCategory)" class="cursor-pointer">{{ selectedCategory.name }}</a>
          </li>
          <li v-for="item in breadcrumb" :key="`${item.type}-${item.id}`">
            <a @click="navigateToBreadcrumb(item)" class="cursor-pointer">{{ item.name }}</a>
          </li>
        </ul>
      </div>

      <!-- Actions Bar -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex gap-2">
          <button @click="resetView" class="btn btn-ghost btn-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Volver
          </button>
        </div>
        
        <div class="form-control">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar archivos..." 
            class="input input-bordered input-sm w-64"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-error">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ error }}</span>
      </div>

      <!-- Files Table -->
      <div v-else class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Tamaño</th>
              <th>Licencia</th>
              <th>Modificado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <!-- Directories -->
            <tr v-for="dir in filteredDirectories" :key="`dir-${dir.id}`" class="hover">
              <td>
                <div class="flex items-center space-x-3 cursor-pointer" @click="selectDirectory(dir)">
                  <div class="avatar">
                    <div class="w-10 h-10 bg-base-200 rounded flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <div>
                    <div class="font-bold hover:text-primary">
                      {{ dir.name }}
                      <svg v-if="!dir.is_public" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                  </div>
                </div>
              </td>
              <td>Carpeta</td>
              <td>{{ dir.files_count }} archivos</td>
              <td>-</td>
              <td>{{ formatDate(dir.created_at) }}</td>
              <td>
                <button 
                  @click="downloadDirectory(dir)"
                  class="btn btn-ghost btn-xs"
                  title="Descargar como ZIP"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                  </svg>
                </button>
              </td>
            </tr>

            <!-- Files -->
            <tr v-for="file in filteredFiles" :key="`file-${file.id}`" class="hover">
              <td>
                <div class="flex items-center space-x-3">
                  <div class="avatar">
                    <div class="w-10 h-10 bg-base-200 rounded flex items-center justify-center">
                      <svg v-if="getFileIcon(file) === 'pdf'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      <svg v-else-if="getFileIcon(file) === 'image'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <div>
                    <div class="font-bold">
                      {{ file.name }}
                      <svg v-if="!file.is_public" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <div v-if="file.description" class="text-sm text-gray-500">{{ file.description }}</div>
                  </div>
                </div>
              </td>
              <td>{{ file.extension }}</td>
              <td>{{ file.size_display }}</td>
              <td>
                <span class="badge badge-success badge-sm">
                  {{ file.license_display }}
                </span>
              </td>
              <td>{{ formatDate(file.uploaded_at) }}</td>
              <td>
                <div class="flex gap-1">
                  <button 
                    v-if="file.can_preview"
                    @click="previewFile(file)"
                    class="btn btn-ghost btn-xs"
                    title="Vista previa"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button 
                    @click="downloadFile(file)"
                    class="btn btn-ghost btn-xs"
                    title="Descargar"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredItems.length === 0" class="text-center py-16">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <h3 class="text-xl font-semibold mb-2">No hay archivos en esta carpeta</h3>
        <p class="text-gray-600">No se encontraron archivos o carpetas</p>
      </div>
    </div>

    <!-- Preview Modal -->
    <dialog ref="previewModal" class="modal">
      <div class="modal-box max-w-4xl">
        <h3 class="font-bold text-lg mb-4">{{ selectedFile?.name }}</h3>
        
        <!-- PDF Preview -->
        <iframe 
          v-if="selectedFile?.extension === 'PDF'"
          :src="previewUrl"
          class="w-full h-[600px]"
        ></iframe>
        
        <!-- Image Preview -->
        <img 
          v-else-if="['JPG', 'JPEG', 'PNG', 'GIF', 'SVG'].includes(selectedFile?.extension)"
          :src="previewUrl"
          class="w-full"
        />
        
        <!-- Text Preview -->
        <pre 
          v-else-if="['TXT', 'MD'].includes(selectedFile?.extension)"
          class="bg-base-200 p-4 rounded overflow-auto max-h-[600px]"
        >{{ previewContent }}</pre>
        
        <div class="modal-action">
          <button @click="closePreview" class="btn">Cerrar</button>
          <button @click="downloadFile(selectedFile)" class="btn btn-primary">Descargar</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="closePreview">close</button>
      </form>
    </dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()

// State
const categories = ref([])
const selectedCategory = ref(null)
const currentDirectory = ref(null)
const directories = ref([])
const files = ref([])
const breadcrumb = ref([])
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)
const previewModal = ref(null)
const selectedFile = ref(null)
const previewUrl = ref('')
const previewContent = ref('')

// Computed
const filteredItems = computed(() => {
  const items = [...directories.value, ...files.value]
  
  if (!searchQuery.value) return items
  
  return items.filter(item => 
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const filteredDirectories = computed(() => {
  if (!searchQuery.value) return directories.value
  
  return directories.value.filter(dir => 
    dir.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const filteredFiles = computed(() => {
  if (!searchQuery.value) return files.value
  
  return files.value.filter(file => 
    file.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (file.description && file.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
})

// Methods
const loadCategories = async () => {
  try {
    const response = await api.get('/repositorio/categories/')
    categories.value = response.data.results || response.data
  } catch (err) {
    toast.error('Error al cargar las categorías')
    console.error(err)
  }
}

const selectCategory = async (category) => {
  selectedCategory.value = category
  currentDirectory.value = null
  breadcrumb.value = []
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(`/repositorio/categories/${category.slug}/`)
    console.log('Category response:', response.data)
    directories.value = response.data.root_directories || []
    files.value = response.data.root_files || []
    console.log('Directories loaded:', directories.value)
    console.log('Files loaded:', files.value)
  } catch (err) {
    error.value = 'Error al cargar el contenido de la categoría'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const selectDirectory = async (directory) => {
  currentDirectory.value = directory
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get(`/repositorio/directories/${directory.id}/`)
    directories.value = response.data.subdirectories || []
    files.value = response.data.files || []
    
    // Update breadcrumb
    await updateBreadcrumb('directory', directory.id)
  } catch (err) {
    error.value = 'Error al cargar el contenido del directorio'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const updateBreadcrumb = async (type, id) => {
  try {
    const response = await api.get('/repositorio/breadcrumb/', {
      params: { type, id }
    })
    breadcrumb.value = response.data.slice(1) // Remove category from breadcrumb
  } catch (err) {
    console.error('Error updating breadcrumb:', err)
  }
}

const navigateToBreadcrumb = (item) => {
  if (item.type === 'directory') {
    selectDirectory({ id: item.id })
  }
}

const resetView = () => {
  selectedCategory.value = null
  currentDirectory.value = null
  directories.value = []
  files.value = []
  breadcrumb.value = []
  searchQuery.value = ''
}

const getFileIcon = (file) => {
  if (['pdf'].includes(file.icon)) return 'pdf'
  if (['image'].includes(file.icon)) return 'image'
  return 'file'
}

const downloadFile = async (file) => {
  try {
    const response = await api.get(`/repositorio/files/${file.id}/download/`, {
      responseType: 'blob'
    })
    
    // Create download link with proper mime type
    const blob = new Blob([response.data], { type: response.headers['content-type'] || file.mime_type })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.download_name || file.name)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success(`Descargando ${file.download_name || file.name}`)
  } catch (err) {
    toast.error('Error al descargar el archivo')
    console.error(err)
  }
}

const downloadDirectory = async (directory) => {
  try {
    const response = await api.get(`/repositorio/directories/${directory.id}/download/`, {
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${directory.name}.zip`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success(`Descargando ${directory.name}.zip`)
  } catch (err) {
    toast.error('Error al descargar el directorio')
    console.error(err)
  }
}

const previewFile = async (file) => {
  selectedFile.value = file
  
  if (['PDF', 'JPG', 'JPEG', 'PNG', 'GIF', 'SVG'].includes(file.extension)) {
    previewUrl.value = `/api/v1/repositorio/files/${file.id}/preview/`
  } else if (['TXT', 'MD'].includes(file.extension)) {
    try {
      const response = await api.get(`/repositorio/files/${file.id}/preview/`)
      previewContent.value = response.data.content
    } catch (err) {
      toast.error('Error al cargar la vista previa')
      return
    }
  }
  
  previewModal.value.showModal()
}

const closePreview = () => {
  previewModal.value.close()
  selectedFile.value = null
  previewUrl.value = ''
  previewContent.value = ''
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

// Lifecycle
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-4px);
}
</style>