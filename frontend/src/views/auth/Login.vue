<template>
  <div class="card w-full bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-2xl font-bold text-center mb-6">Iniciar Sesión</h2>
      
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Usuario o Email</span>
          </label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="Ingresa tu usuario o email" 
            class="input input-bordered w-full" 
            :class="{ 'input-error': errors.username }"
            required
          />
          <label v-if="errors.username" class="label">
            <span class="label-text-alt text-error">{{ errors.username }}</span>
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Contraseña</span>
          </label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="Ingresa tu contraseña" 
            class="input input-bordered w-full" 
            :class="{ 'input-error': errors.password }"
            required
          />
          <label v-if="errors.password" class="label">
            <span class="label-text-alt text-error">{{ errors.password }}</span>
          </label>
          <label class="label">
            <a href="#" class="label-text-alt link link-hover">¿Olvidaste tu contraseña?</a>
          </label>
        </div>

        <div v-if="errors.general" class="alert alert-error">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ errors.general }}</span>
        </div>

        <div class="form-control mt-6">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </div>
      </form>

      <div class="divider">O</div>

      <div class="text-center">
        <p class="text-sm">
          ¿No tienes una cuenta? 
          <router-link :to="{ name: 'Register' }" class="link link-primary">
            Regístrate aquí
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const errors = reactive({
  username: '',
  password: '',
  general: ''
})

const loading = ref(false)

const clearErrors = () => {
  errors.username = ''
  errors.password = ''
  errors.general = ''
}

const handleLogin = async () => {
  clearErrors()
  loading.value = true

  const result = await authStore.login({
    username: form.username,
    password: form.password
  })

  loading.value = false

  if (result.success) {
    const redirectTo = route.query.redirect || '/'
    router.push(redirectTo)
  } else {
    errors.general = result.error || 'Error al iniciar sesión'
  }
}
</script>