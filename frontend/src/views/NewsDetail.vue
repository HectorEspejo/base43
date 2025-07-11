<template>
  <div class="min-h-screen">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-96">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container-custom mx-auto section-padding py-8">
      <div class="alert alert-error">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ error }}</span>
      </div>
      <div class="mt-4">
        <router-link to="/noticias" class="btn btn-ghost">
          ← Volver a noticias
        </router-link>
      </div>
    </div>

    <!-- News Content -->
    <article v-else-if="newsPost">
      <!-- Header Image with Title Overlay -->
      <div class="relative h-[400px] md:h-[500px] w-full">
        <img 
          :src="newsPost.header_image_url || 'https://placehold.co/1200x600'" 
          :alt="newsPost.title"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
        <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
          <div class="container-custom mx-auto">
            <div class="badge badge-primary mb-4">{{ newsPost.category }}</div>
            <h1 class="text-3xl md:text-5xl font-bold mb-4">{{ newsPost.title }}</h1>
            <div class="flex items-center gap-4 text-sm md:text-base">
              <span>Por {{ newsPost.author.first_name }} {{ newsPost.author.last_name }}</span>
              <span>•</span>
              <span>{{ formatDate(newsPost.created_at) }}</span>
              <span>•</span>
              <span class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                {{ newsPost.views }} vistas
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <div class="container-custom mx-auto section-padding py-8">
        <div class="max-w-4xl mx-auto">
          <!-- Breadcrumb -->
          <div class="breadcrumbs text-sm mb-6">
            <ul>
              <li><router-link to="/">Inicio</router-link></li>
              <li><router-link to="/noticias">Noticias</router-link></li>
              <li class="text-gray-600">{{ newsPost.title }}</li>
            </ul>
          </div>

          <!-- Excerpt -->
          <div class="text-lg text-gray-700 font-medium mb-8 border-l-4 border-primary pl-4">
            {{ newsPost.excerpt }}
          </div>

          <!-- Main Content -->
          <div 
            class="prose prose-lg max-w-none article-content"
            v-html="newsPost.content"
          ></div>

          <!-- Author Info -->
          <div class="mt-12 p-6 bg-base-200 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Sobre el autor</h3>
            <div class="flex items-center gap-4">
              <div class="avatar">
                <div class="w-16 rounded-full">
                  <img 
                    :src="newsPost.author.avatar || 'https://placehold.co/150x150'" 
                    :alt="`${newsPost.author.first_name} ${newsPost.author.last_name}`"
                  />
                </div>
              </div>
              <div>
                <p class="font-semibold">{{ newsPost.author.first_name }} {{ newsPost.author.last_name }}</p>
                <p class="text-sm text-gray-600">{{ newsPost.author.email }}</p>
                <p v-if="newsPost.author.bio" class="text-sm mt-1">{{ newsPost.author.bio }}</p>
              </div>
            </div>
          </div>

          <!-- Updated Date -->
          <div v-if="newsPost.updated_at !== newsPost.created_at" class="text-sm text-gray-500 mt-6">
            Última actualización: {{ formatDate(newsPost.updated_at) }}
          </div>

          <!-- Navigation -->
          <div class="flex justify-between items-center mt-12 pt-8 border-t">
            <router-link to="/noticias" class="btn btn-ghost">
              ← Volver a noticias
            </router-link>
            <div class="flex gap-2">
              <button class="btn btn-circle btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m9.032 4.026a9 9 0 10-13.432 0m13.432 0A9 9 0 0112 21m0 0a9 9 0 01-5.432-1.842m10.864 0A9 9 0 0112 21" />
                </svg>
              </button>
              <button class="btn btn-circle btn-ghost">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

// Route params
const route = useRoute()

// State
const newsPost = ref(null)
const loading = ref(true)
const error = ref(null)

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const fetchNewsPost = async () => {
  try {
    const { slug } = route.params
    const response = await api.get(`/noticias/${slug}/`)
    newsPost.value = response.data
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = 'No se encontró la noticia solicitada.'
    } else {
      error.value = 'Error al cargar la noticia. Por favor, intenta de nuevo.'
    }
    console.error('Error fetching news post:', err)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchNewsPost()
})
</script>

<style scoped>
/* Custom styles for article content */
:deep(.article-content) {
  @apply text-gray-700;
}

:deep(.article-content h1),
:deep(.article-content h2),
:deep(.article-content h3),
:deep(.article-content h4),
:deep(.article-content h5),
:deep(.article-content h6) {
  @apply font-bold text-gray-900 mb-4 mt-8;
}

:deep(.article-content p) {
  @apply mb-4 leading-relaxed;
}

:deep(.article-content img) {
  @apply rounded-lg shadow-md my-6 max-w-full h-auto;
}

:deep(.article-content ul),
:deep(.article-content ol) {
  @apply mb-4 ml-6;
}

:deep(.article-content li) {
  @apply mb-2;
}

:deep(.article-content blockquote) {
  @apply border-l-4 border-l-blue-500 pl-4 italic my-6;
}

:deep(.article-content a) {
  @apply text-blue-600 hover:underline;
}

:deep(.article-content table) {
  @apply table table-zebra w-full my-6;
}

:deep(.article-content th) {
  @apply bg-base-200;
}

:deep(.article-content td),
:deep(.article-content th) {
  @apply px-4 py-2;
}
</style>