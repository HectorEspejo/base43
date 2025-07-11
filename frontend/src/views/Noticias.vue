<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Noticias y Actualizaciones</h1>
    
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

    <!-- Content -->
    <template v-else>
      <!-- Featured News -->
      <div v-if="featuredNews" class="card lg:card-side bg-base-100 shadow-xl mb-8">
        <figure class="lg:w-1/2">
          <img 
            :src="featuredNews.header_image_url || 'https://placehold.co/800x400'" 
            :alt="featuredNews.title"
            class="h-full w-full object-cover"
          />
        </figure>
        <div class="card-body lg:w-1/2">
          <div class="badge badge-primary mb-2">Destacado</div>
          <h2 class="card-title text-2xl">{{ featuredNews.title }}</h2>
          <p class="text-gray-600">{{ formatDate(featuredNews.created_at) }} • {{ featuredNews.author_name }}</p>
          <p class="mt-4">{{ featuredNews.excerpt }}</p>
          <div class="card-actions justify-end mt-6">
            <router-link 
              :to="`/noticias/${getDateParts(featuredNews.created_at)}/${featuredNews.slug}`"
              class="btn btn-primary"
            >
              Leer más
            </router-link>
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
              :src="article.header_image_url || 'https://placehold.co/400x200'" 
              :alt="article.title"
              class="h-48 w-full object-cover"
            />
          </figure>
          <div class="card-body">
            <div class="flex gap-2 mb-2">
              <span class="badge badge-sm badge-outline">{{ article.category }}</span>
            </div>
            <h2 class="card-title text-lg">{{ article.title }}</h2>
            <p class="text-sm text-gray-600">{{ formatDate(article.created_at) }}</p>
            <p class="mt-2 line-clamp-3">{{ article.excerpt }}</p>
            <div class="card-actions justify-between items-center mt-4">
              <div class="flex items-center gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  {{ article.views }}
                </span>
              </div>
              <router-link 
                :to="`/noticias/${getDateParts(article.created_at)}/${article.slug}`"
                class="btn btn-ghost btn-sm"
              >
                Leer →
              </router-link>
            </div>
          </div>
        </article>
      </div>

      <!-- Load More -->
      <div v-if="hasMore" class="text-center mt-8">
        <button 
          @click="loadMore" 
          :disabled="loadingMore"
          class="btn btn-outline"
        >
          <span v-if="loadingMore" class="loading loading-spinner"></span>
          <span v-else>Cargar más noticias</span>
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && news.length === 0" class="text-center py-12">
        <p class="text-gray-500">No hay noticias disponibles en este momento.</p>
      </div>
    </template>

    <!-- Newsletter Subscription -->
    <div class="card bg-primary text-primary-content mt-12">
      <div class="card-body text-center">
        <h2 class="card-title text-2xl justify-center mb-4">Suscríbete a nuestro boletín</h2>
        <p class="mb-6">Recibe las últimas noticias y actualizaciones directamente en tu correo</p>
        <div class="form-control">
          <label class="input-group justify-center">
            <input 
              type="email" 
              v-model="newsletterEmail"
              placeholder="tu@email.com" 
              class="input input-bordered text-base-content w-full max-w-xs" 
            />
            <button 
              @click="subscribeNewsletter"
              class="btn btn-secondary"
            >
              Suscribir
            </button>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()

// State
const news = ref([])
const featuredNews = ref(null)
const loading = ref(true)
const loadingMore = ref(false)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const newsletterEmail = ref('')

// Computed
const hasMore = computed(() => currentPage.value < totalPages.value)

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const getDateParts = (dateString) => {
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}/${month}/${day}`
}

const fetchNews = async (page = 1) => {
  try {
    const response = await api.get('/noticias/', {
      params: {
        page,
        page_size: 6
      }
    })
    
    if (page === 1) {
      news.value = response.data.results
      // Find featured news
      const featured = news.value.find(item => item.featured)
      if (featured) {
        featuredNews.value = featured
        news.value = news.value.filter(item => item.id !== featured.id)
      }
    } else {
      news.value.push(...response.data.results)
    }
    
    currentPage.value = page
    totalPages.value = Math.ceil(response.data.count / 6)
  } catch (err) {
    error.value = 'Error al cargar las noticias. Por favor, intenta de nuevo.'
    console.error('Error fetching news:', err)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = async () => {
  loadingMore.value = true
  await fetchNews(currentPage.value + 1)
}

const subscribeNewsletter = async () => {
  if (!newsletterEmail.value) {
    toast.error('Por favor ingresa tu correo electrónico')
    return
  }
  
  // TODO: Implement newsletter subscription
  toast.success('¡Gracias por suscribirte! Te mantendremos informado.')
  newsletterEmail.value = ''
}

// Lifecycle
onMounted(() => {
  fetchNews()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>