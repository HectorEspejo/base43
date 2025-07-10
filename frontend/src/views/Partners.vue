<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Nuestros partners</h1>
    
    <p class="text-lg mb-12 max-w-3xl">
      Trabajamos con organizaciones comprometidas con la transformación del modelo de vivienda, 
      promoviendo alternativas sostenibles, colaborativas y centradas en las personas.
    </p>

    <!-- Partners Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
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
          <div class="badge badge-outline mb-2">{{ partner.type }}</div>
          <p>{{ partner.description }}</p>
          
          <div class="mt-4 text-sm">
            <p class="font-semibold">Áreas de trabajo:</p>
            <div class="flex flex-wrap gap-2 justify-center mt-2">
              <span 
                v-for="area in partner.areas" 
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
            <button class="btn btn-sm btn-primary">Contactar</button>
          </div>
        </div>
      </div>
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
          <h3 class="font-semibold mb-2">Red de Contactos</h3>
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
          <h3 class="font-semibold mb-2">Recursos Compartidos</h3>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Mock data - replace with API call
const partners = ref([
  {
    id: 1,
    name: 'AdobeVerde',
    type: 'Empresa de inserción',
    description: 'Cooperativa especializada en construcción sostenible con técnicas tradicionales y materiales ecológicos.',
    areas: ['Construcción', 'Sostenibilidad', 'Formación'],
    website: 'https://adobeverde.eu',
    logo: '/adobeverde.png'
  },
  {
    id: 2,
    name: 'Prodiversa',
    type: 'Asociación',
    description: 'Promoción de la diversidad en proyectos de vivienda inclusiva y accesible para todos.',
    areas: ['Inclusión', 'Accesibilidad', 'Diseño Universal'],
    website: 'https://prodiversa.eu',
    logo: '/prodiversa.jpg'
  },
  {
    id: 3,
    name: 'Universidad de Málaga',
    type: 'Institución',
    description: 'Colaboración con diversas facultades en la investigación y desarrollo del proyecto.',
    areas: ['Vivienda Social', 'Cesión de Uso', 'Asesoría'],
    website: null,
    logo: 'uma.jpg'
  },
  {
    id: 4,
    name: 'EcoHabitar',
    type: 'Fundación',
    description: 'Fundación dedicada a la investigación y promoción de hábitats sostenibles y resilientes.',
    areas: ['Investigación', 'Permacultura', 'Educación'],
    website: 'https://ecohabitar.org',
    logo: null
  },
  {
    id: 5,
    name: 'Financoop',
    type: 'Entidad Financiera',
    description: 'Cooperativa de crédito especializada en financiación ética para proyectos de economía social.',
    areas: ['Financiación', 'Banca Ética', 'Asesoría Financiera'],
    website: null,
    logo: null
  },
  {
    id: 6,
    name: 'ArquiSocial',
    type: 'Estudio',
    description: 'Estudio de arquitectura especializado en procesos participativos y diseño colaborativo.',
    areas: ['Arquitectura', 'Participación', 'Diseño Social'],
    website: 'https://arquisocial.com',
    logo: null
  }
])
</script>