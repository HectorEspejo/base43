<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Contacto</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Contact Form -->
      <div>
        <h2 class="text-2xl font-semibold mb-6">Envíanos un mensaje</h2>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text">Nombre</span>
              </label>
              <input 
                v-model="form.name" 
                type="text" 
                placeholder="Tu nombre" 
                class="input input-bordered w-full" 
                required
              />
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">Apellidos</span>
              </label>
              <input 
                v-model="form.surname" 
                type="text" 
                placeholder="Tus apellidos" 
                class="input input-bordered w-full" 
                required
              />
            </div>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="tu@email.com" 
              class="input input-bordered w-full" 
              required
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Teléfono (opcional)</span>
            </label>
            <input 
              v-model="form.phone" 
              type="tel" 
              placeholder="+34 600 000 000" 
              class="input input-bordered w-full" 
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Asunto</span>
            </label>
            <select v-model="form.subject" class="select select-bordered w-full" required>
              <option value="">Selecciona un asunto</option>
              <option value="informacion">Información general</option>
              <option value="proyecto">Sobre un proyecto</option>
              <option value="colaboracion">Propuesta de colaboración</option>
              <option value="tecnico">Soporte técnico</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Mensaje</span>
            </label>
            <textarea 
              v-model="form.message" 
              class="textarea textarea-bordered h-32" 
              placeholder="Escribe tu mensaje aquí..."
              required
            ></textarea>
          </div>

          <div class="form-control">
            <label class="cursor-pointer label justify-start">
              <input v-model="form.privacy" type="checkbox" class="checkbox checkbox-primary mr-2" required />
              <span class="label-text">
                He leído y acepto la <router-link :to="{ name: 'Privacidad' }" class="link link-primary" target="_blank">política de privacidad</router-link>
              </span>
            </label>
          </div>

          <div class="form-control mt-6">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner"></span>
              {{ loading ? 'Enviando...' : 'Enviar mensaje' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Contact Information -->
      <div>
        <h2 class="text-2xl font-semibold mb-6">Información de contacto</h2>
        
        <div class="space-y-6">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold mb-1">Email</h3>
              <p class="text-gray-600">contacto@base43.org</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold mb-1">Teléfono</h3>
              <p class="text-gray-600">+34 652 615 416</p>
              <p class="text-sm text-gray-500">Lunes a viernes: 9:00 - 15:30</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-accent bg-opacity-20 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold mb-1">Dirección</h3>
              <p class="text-gray-600">Calle Juan del Encina, 24, Local 1</p>
              <p class="text-gray-600">29013 Málaga, España</p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-info bg-opacity-20 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold mb-1">Horario de atención</h3>
              <p class="text-gray-600">Lunes a Viernes: 9:00 - 15:30</p>
            </div>
          </div>
        </div>

        <!-- Social Media -->
        <div class="mt-8">
          <h3 class="font-semibold mb-4">Síguenos en redes sociales</h3>
          <div class="flex gap-4">
            <a href="https://www.facebook.com/p/Adobe-Verde-100093504368739/" class="btn btn-circle btn-outline">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="https://www.instagram.com/base43" class="btn btn-circle btn-outline">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1112.324 0 6.162 6.162 0 01-12.324 0zM12 16a4 4 0 110-8 4 4 0 010 8zm4.965-10.405a1.44 1.44 0 112.881.001 1.44 1.44 0 01-2.881-.001z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const toast = useToast()
const loading = ref(false)

const form = reactive({
  name: '',
  surname: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  privacy: false
})

const handleSubmit = async () => {
  loading.value = true
  
  try {
    const response = await api.post('/contacto/send/', form)
    
    if (response.data.success) {
      toast.success(response.data.message || 'Mensaje enviado correctamente. Te responderemos lo antes posible.')
      
      // Reset form
      Object.keys(form).forEach(key => {
        if (typeof form[key] === 'boolean') {
          form[key] = false
        } else {
          form[key] = ''
        }
      })
    }
  } catch (error) {
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.detail || 
                        'Error al enviar el mensaje. Por favor, inténtalo de nuevo.'
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>