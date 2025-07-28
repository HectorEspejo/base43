<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Nuestros partners</h1>
    
    <p class="text-lg mb-12 max-w-3xl">
      Trabajamos con organizaciones comprometidas con la transformación del modelo de vivienda, 
      promoviendo alternativas sostenibles, colaborativas y centradas en las personas.
    </p>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-16">
      <span class="loading loading-spinner loading-lg"></span>
      <p class="text-gray-600 mt-2">Cargando partners...</p>
    </div>

    <!-- Partners Grid -->
    <div v-else-if="partners.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div 
        v-for="partner in partners" 
        :key="partner.id" 
        class="card bg-base-100 shadow-xl card-hover"
      >
        <figure class="px-10 pt-10">
          <div class="w-32 h-32 bg-base-200 rounded-full flex items-center justify-center">
            <img 
              v-if="partner.logo" 
              :src="partner.logo" 
              :alt="partner.name"
              class="rounded-full"
            />
            <span v-else class="text-4xl font-bold text-primary">
              {{ partner.name.charAt(0) }}
            </span>
          </div>
        </figure>
        <div class="card-body items-center text-center">
          <h2 class="card-title">{{ partner.name }}</h2>
          <div class="badge badge-outline mb-2">{{ partner.partner_type_display || partner.partner_type }}</div>
          <p v-if="partner.location" class="text-sm text-gray-600 mb-2">{{ partner.location }}</p>
          <p class="line-clamp-3">{{ partner.description }}</p>
          
          <div v-if="partner.collaboration_areas_list && partner.collaboration_areas_list.length > 0" class="mt-4 text-sm">
            <p class="font-semibold">Áreas de colaboración:</p>
            <div class="flex flex-wrap gap-2 justify-center mt-2">
              <span 
                v-for="area in partner.collaboration_areas_list" 
                :key="area"
                class="badge badge-sm badge-secondary"
              >
                {{ area }}
              </span>
            </div>
          </div>
          
          <div class="card-actions mt-6">
            <a 
              v-if="partner.website" 
              :href="partner.website" 
              target="_blank"
              class="btn btn-sm btn-outline"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              Visitar web
            </a>
            <button @click="openPartnerModal(partner)" class="btn btn-sm btn-primary">Ver más</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <h3 class="text-xl font-semibold mb-2">No hay partners disponibles</h3>
      <p class="text-gray-600">Pronto añadiremos información sobre nuestros colaboradores</p>
    </div>

    <!-- Become a Partner CTA -->
    <div class="card bg-gradient-to-r from-primary to-secondary text-white mt-16">
      <div class="card-body text-center">
        <h2 class="card-title text-3xl justify-center mb-4">¿Quieres ser partner?</h2>
        <p class="mb-6 max-w-2xl mx-auto">
          Si tu organización comparte nuestra visión de transformar el modelo de vivienda 
          y quiere colaborar con nosotros, nos encantaría conocerte.
        </p>
        <div class="card-actions justify-center">
          <button class="btn btn-lg bg-white text-primary hover:bg-gray-100">
          <router-link :to="{ name: 'Contacto' }" class="btn btn-primary btn-lg">
            Solicitar información
          </router-link>
          </button>
        </div>
      </div>
    </div>

    <!-- Partner Benefits -->
    <div class="mt-16">
      <h2 class="text-3xl font-bold text-center mb-12">Beneficios de ser Partner</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="text-center">
          <div class="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="font-semibold mb-2">Red de contactos</h3>
          <p class="text-sm text-gray-600">Acceso a una amplia red de profesionales y organizaciones del sector</p>
        </div>
        
        <div class="text-center">
          <div class="w-16 h-16 bg-secondary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-secondary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="font-semibold mb-2">Visibilidad</h3>
          <p class="text-sm text-gray-600">Promoción de tu organización en nuestra plataforma y eventos</p>
        </div>
        
        <div class="text-center">
          <div class="w-16 h-16 bg-accent bg-opacity-20 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 class="font-semibold mb-2">Recursos compartidos</h3>
          <p class="text-sm text-gray-600">Acceso a herramientas, documentación y conocimiento colectivo</p>
        </div>
        
        <div class="text-center">
          <div class="w-16 h-16 bg-info bg-opacity-20 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="font-semibold mb-2">Proyectos conjuntos</h3>
          <p class="text-sm text-gray-600">Oportunidades de colaboración en proyectos innovadores</p>
        </div>
      </div>
    </div>

    <!-- Partner Detail Modal -->
    <div v-if="selectedPartner" class="modal modal-open" @click="closeModal">
      <div class="modal-box max-w-4xl" @click.stop>
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeModal">✕</button>
        
        <div class="text-center mb-6">
          <div v-if="selectedPartner.logo" class="mb-4">
            <img :src="selectedPartner.logo" :alt="selectedPartner.name" class="h-24 w-auto mx-auto" />
          </div>
          <h3 class="font-bold text-2xl mb-2">{{ selectedPartner.name }}</h3>
          <div class="badge badge-secondary">{{ selectedPartner.partner_type_display }}</div>
          <p v-if="selectedPartner.location" class="text-sm text-gray-600 mt-2">{{ selectedPartner.location }}</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-semibold mb-2">Descripción</h4>
            <p class="text-gray-700">{{ selectedPartner.description }}</p>
            
            <div v-if="selectedPartner.mission" class="mt-4">
              <h4 class="font-semibold mb-2">Misión</h4>
              <p class="text-gray-700">{{ selectedPartner.mission }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Información de contacto</h4>
            <div class="space-y-2 text-sm">
              <p v-if="selectedPartner.contact_person"><span class="font-medium">Persona de contacto:</span> {{ selectedPartner.contact_person }}</p>
              <p v-if="selectedPartner.email"><span class="font-medium">Email:</span> <a :href="`mailto:${selectedPartner.email}`" class="link link-primary">{{ selectedPartner.email }}</a></p>
              <p v-if="selectedPartner.phone"><span class="font-medium">Teléfono:</span> {{ selectedPartner.phone }}</p>
              <p v-if="selectedPartner.address"><span class="font-medium">Dirección:</span> {{ selectedPartner.address }}</p>
            </div>
            
            <div v-if="selectedPartner.social_media_links && Object.keys(selectedPartner.social_media_links).length > 0" class="mt-4">
              <h4 class="font-semibold mb-2">Redes sociales</h4>
              <div class="flex gap-2">
                <a v-if="selectedPartner.social_media_links.linkedin" :href="selectedPartner.social_media_links.linkedin" target="_blank" class="btn btn-sm btn-circle">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                </a>
                <a v-if="selectedPartner.social_media_links.twitter" :href="selectedPartner.social_media_links.twitter" target="_blank" class="btn btn-sm btn-circle">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M22.46 6c-.85.38-1.78.64-2.75.76 1-.6 1.76-1.55 2.12-2.68-.93.55-1.96.95-3.06 1.17-.88-.94-2.13-1.53-3.51-1.53-2.66 0-4.81 2.16-4.81 4.81 0 .38.04.75.13 1.1-4-.2-7.58-2.11-9.96-5.02-.42.72-.66 1.56-.66 2.46 0 1.67.85 3.14 2.14 4.01-.79-.02-1.53-.24-2.18-.6v.06c0 2.33 1.66 4.28 3.86 4.72-.4.11-.83.17-1.27.17-.31 0-.62-.03-.91-.08.62 1.91 2.39 3.3 4.5 3.34-1.65 1.29-3.73 2.06-5.99 2.06-.39 0-.77-.02-1.15-.07 2.13 1.36 4.66 2.16 7.39 2.16 8.87 0 13.72-7.35 13.72-13.72 0-.21 0-.42-.01-.62.94-.68 1.76-1.53 2.41-2.5z"/></svg>
                </a>
                <a v-if="selectedPartner.social_media_links.facebook" :href="selectedPartner.social_media_links.facebook" target="_blank" class="btn btn-sm btn-circle">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a v-if="selectedPartner.social_media_links.instagram" :href="selectedPartner.social_media_links.instagram" target="_blank" class="btn btn-sm btn-circle">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1 1 12.324 0 6.162 6.162 0 0 1-12.324 0zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm4.965-10.405a1.44 1.44 0 1 1 2.881.001 1.44 1.44 0 0 1-2.881-.001z"/></svg>
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="selectedPartner.collaboration_areas_list && selectedPartner.collaboration_areas_list.length > 0" class="mt-6">
          <h4 class="font-semibold mb-2">Áreas de colaboración</h4>
          <div class="flex flex-wrap gap-2">
            <span v-for="area in selectedPartner.collaboration_areas_list" :key="area" class="badge badge-secondary">
              {{ area }}
            </span>
          </div>
        </div>
        
        <div v-if="selectedPartner.partner_projects && selectedPartner.partner_projects.length > 0" class="mt-6">
          <h4 class="font-semibold mb-2">Proyectos en los que colabora</h4>
          <div class="space-y-2">
            <div v-for="project in selectedPartner.partner_projects" :key="project.id" class="border-l-2 border-primary pl-4">
              <p class="font-medium">{{ project.project_name }}</p>
              <p class="text-sm text-gray-600">{{ project.role }}</p>
            </div>
          </div>
        </div>
        
        <div class="modal-action">
          <a v-if="selectedPartner.website" :href="selectedPartner.website" target="_blank" class="btn btn-primary">
            Visitar sitio web
          </a>
          <router-link :to="{ name: 'Contacto' }" class="btn btn-secondary">
            Contactar
          </router-link>
          <button class="btn" @click="closeModal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()

// State
const partners = ref([])
const loading = ref(false)
const categories = ref([])
const selectedPartner = ref(null)

// Fetch partners from API
const fetchPartners = async () => {
  loading.value = true
  try {
    const response = await api.get('/partners/partners/')
    partners.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching partners:', error)
    toast.error('Error al cargar los partners')
  } finally {
    loading.value = false
  }
}

// Get partner details
const getPartnerDetails = async (partner) => {
  if (!partner || !partner.slug) {
    console.error('Invalid partner:', partner)
    toast.error('Partner inválido')
    return
  }
  
  try {
    const response = await api.get(`/partners/partners/${partner.slug}/`)
    selectedPartner.value = response.data
  } catch (error) {
    console.error('Error fetching partner details:', error)
    toast.error('Error al cargar los detalles del partner')
    selectedPartner.value = null
  }
}

// Open partner modal
const openPartnerModal = (partner) => {
  getPartnerDetails(partner)
}

// Close modal
const closeModal = () => {
  selectedPartner.value = null
}

// Initialize
onMounted(() => {
  fetchPartners()
})
</script>

<style scoped>
.card-hover {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>