<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Repositorio de Documentos</h1>
    
    <!-- Breadcrumb -->
    <div class="text-sm breadcrumbs mb-6">
      <ul>
        <li><a @click="navigateToFolder('')">Inicio</a></li>
        <li v-for="(folder, index) in breadcrumb" :key="index">
          <a @click="navigateToFolder(folder.path)">{{ folder.name }}</a>
        </li>
      </ul>
    </div>

    <!-- Actions Bar -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex gap-2">
        <button class="btn btn-primary btn-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          Subir archivo
        </button>
        <button class="btn btn-outline btn-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          Nueva carpeta
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

    <!-- Files Table -->
    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>
              <label>
                <input type="checkbox" class="checkbox" />
              </label>
            </th>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Tamaño</th>
            <th>Licencia</th>
            <th>Modificado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id" class="hover">
            <th>
              <label>
                <input type="checkbox" class="checkbox" />
              </label>
            </th>
            <td>
              <div class="flex items-center space-x-3">
                <div class="avatar">
                  <div class="w-10 h-10 bg-base-200 rounded flex items-center justify-center">
                    <svg v-if="item.type === 'folder'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <div class="font-bold cursor-pointer hover:text-primary" @click="handleItemClick(item)">
                    {{ item.name }}
                  </div>
                </div>
              </div>
            </td>
            <td>{{ item.type === 'folder' ? 'Carpeta' : item.extension }}</td>
            <td>{{ item.type === 'folder' ? '-' : formatFileSize(item.size) }}</td>
            <td>
              <span v-if="item.type !== 'folder'" class="badge badge-success badge-sm">
                {{ item.license || 'CC-BY-SA' }}
              </span>
            </td>
            <td>{{ formatDate(item.modified) }}</td>
            <td>
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-ghost btn-xs">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                </label>
                <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                  <li><a>Descargar</a></li>
                  <li><a>Compartir</a></li>
                  <li><a>Renombrar</a></li>
                  <li><a>Mover</a></li>
                  <li><a class="text-error">Eliminar</a></li>
                </ul>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-if="filteredItems.length === 0" class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No hay archivos en esta carpeta</h3>
      <p class="text-gray-600">Sube archivos o crea carpetas para comenzar</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const searchQuery = ref('')
const currentPath = ref('')
const breadcrumb = ref([])

// Mock data - replace with API call
const items = ref([
  {
    id: 1,
    name: 'Guías de Construcción',
    type: 'folder',
    modified: new Date('2024-01-15')
  },
  {
    id: 2,
    name: 'Manual Cohousing.pdf',
    type: 'file',
    extension: 'PDF',
    size: 2456789,
    license: 'CC-BY-SA',
    modified: new Date('2024-01-10')
  },
  {
    id: 3,
    name: 'Plantilla Estatutos Cooperativa.docx',
    type: 'file',
    extension: 'DOCX',
    size: 156789,
    license: 'CC0',
    modified: new Date('2024-01-08')
  }
])

const filteredItems = computed(() => {
  if (!searchQuery.value) return items.value
  
  return items.value.filter(item => 
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const handleItemClick = (item) => {
  if (item.type === 'folder') {
    navigateToFolder(item.path || item.name)
  } else {
    // TODO: Implement file preview/download
    toast.info(`Abriendo ${item.name}`)
  }
}

const navigateToFolder = (path) => {
  currentPath.value = path
  // TODO: Update breadcrumb and load folder contents
  updateBreadcrumb(path)
}

const updateBreadcrumb = (path) => {
  if (!path) {
    breadcrumb.value = []
    return
  }
  
  const parts = path.split('/')
  breadcrumb.value = parts.map((part, index) => ({
    name: part,
    path: parts.slice(0, index + 1).join('/')
  }))
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}
</script>