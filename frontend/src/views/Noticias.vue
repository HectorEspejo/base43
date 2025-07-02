<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Noticias y Actualizaciones</h1>
    
    <!-- Featured News -->
    <div v-if="featuredNews" class="card lg:card-side bg-base-100 shadow-xl mb-8">
      <figure class="lg:w-1/2">
        <img 
          :src="featuredNews.image || 'https://placehold.co/800x400'" 
          :alt="featuredNews.title"
          class="h-full w-full object-cover"
        />
      </figure>
      <div class="card-body lg:w-1/2">
        <div class="badge badge-primary mb-2">Destacado</div>
        <h2 class="card-title text-2xl">{{ featuredNews.title }}</h2>
        <p class="text-gray-600">{{ formatDate(featuredNews.date) }} • {{ featuredNews.author }}</p>
        <p class="mt-4">{{ featuredNews.excerpt }}</p>
        <div class="card-actions justify-end mt-6">
          <button class="btn btn-primary">Leer más</button>
        </div>
      </div>
    </div>

    <!-- News Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article 
        v-for="article in news" 
        :key="article.id" 
        class="card bg-base-100 shadow-xl card-hover"
      >
        <figure>
          <img 
            :src="article.image || 'https://placehold.co/400x200'" 
            :alt="article.title"
            class="h-48 w-full object-cover"
          />
        </figure>
        <div class="card-body">
          <div class="flex gap-2 mb-2">
            <span class="badge badge-sm badge-outline">{{ article.category }}</span>
          </div>
          <h2 class="card-title text-lg">{{ article.title }}</h2>
          <p class="text-sm text-gray-600">{{ formatDate(article.date) }}</p>
          <p class="mt-2">{{ article.excerpt }}</p>
          <div class="card-actions justify-between items-center mt-4">
            <div class="flex items-center gap-4 text-sm text-gray-500">
              <span class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                {{ article.views }}
              </span>
              <span class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                {{ article.comments }}
              </span>
            </div>
            <button class="btn btn-ghost btn-sm">Leer →</button>
          </div>
        </div>
      </article>
    </div>

    <!-- Load More -->
    <div class="text-center mt-8">
      <button class="btn btn-outline">Cargar más noticias</button>
    </div>

    <!-- Newsletter Subscription -->
    <div class="card bg-primary text-primary-content mt-12">
      <div class="card-body text-center">
        <h2 class="card-title text-2xl justify-center mb-4">Suscríbete a nuestro boletín</h2>
        <p class="mb-6">Recibe las últimas noticias y actualizaciones directamente en tu correo</p>
        <div class="form-control">
          <label class="input-group justify-center">
            <input 
              type="email" 
              placeholder="tu@email.com" 
              class="input input-bordered text-base-content w-full max-w-xs" 
            />
            <button class="btn btn-secondary">Suscribir</button>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Mock data - replace with API call
const featuredNews = ref({
  id: 1,
  title: 'Nueva cooperativa de vivienda inaugura sus instalaciones en Madrid',
  excerpt: 'La cooperativa Las Flores ha completado la construcción de 30 viviendas sostenibles en régimen de cesión de uso, marcando un hito en el modelo de vivienda colaborativa.',
  author: 'María García',
  date: new Date('2024-01-20'),
  category: 'Cooperativas',
  image: null
})

const news = ref([
  {
    id: 2,
    title: 'Guía completa sobre financiación para proyectos de cohousing',
    excerpt: 'Exploramos las diferentes opciones de financiación disponibles para proyectos de vivienda colaborativa.',
    date: new Date('2024-01-18'),
    category: 'Recursos',
    views: 234,
    comments: 12,
    image: null
  },
  {
    id: 3,
    title: 'Taller de diseño participativo este fin de semana',
    excerpt: 'Aprende técnicas de diseño colaborativo para proyectos de vivienda comunitaria.',
    date: new Date('2024-01-15'),
    category: 'Eventos',
    views: 156,
    comments: 8,
    image: null
  },
  {
    id: 4,
    title: 'Cambios en la legislación de cooperativas de vivienda',
    excerpt: 'Analizamos las nuevas modificaciones legales que afectan a las cooperativas.',
    date: new Date('2024-01-12'),
    category: 'Legal',
    views: 432,
    comments: 23,
    image: null
  },
  {
    id: 5,
    title: 'Proyecto intergeneracional busca nuevos miembros',
    excerpt: 'La comunidad Sol Naciente abre convocatoria para familias interesadas.',
    date: new Date('2024-01-10'),
    category: 'Proyectos',
    views: 678,
    comments: 45,
    image: null
  },
  {
    id: 6,
    title: 'Sostenibilidad en la construcción: casos de éxito',
    excerpt: 'Presentamos proyectos que han logrado la certificación Passivhaus.',
    date: new Date('2024-01-08'),
    category: 'Sostenibilidad',
    views: 321,
    comments: 15,
    image: null
  }
])

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
</script>