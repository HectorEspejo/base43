<template>
  <div class="card w-full bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-2xl font-bold text-center mb-6">Crear Cuenta</h2>
      
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Nombre</span>
            </label>
            <input 
              v-model="form.first_name" 
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
              v-model="form.last_name" 
              type="text" 
              placeholder="Tus apellidos" 
              class="input input-bordered w-full" 
              required
            />
          </div>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Nombre de usuario</span>
          </label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="Elige un nombre de usuario" 
            class="input input-bordered w-full" 
            required
          />
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
            <span class="label-text">Tipo de cuenta</span>
          </label>
          <select v-model="form.user_type" class="select select-bordered w-full">
            <option value="individual">Individual</option>
            <option value="organization">Organización</option>
            <option value="partner">Partner</option>
          </select>
        </div>

        <div v-if="form.user_type === 'organization' || form.user_type === 'partner'" class="form-control">
          <label class="label">
            <span class="label-text">Nombre de la organización</span>
          </label>
          <input 
            v-model="form.organization" 
            type="text" 
            placeholder="Nombre de tu organización" 
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
            <span class="label-text">Contraseña</span>
          </label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="Mínimo 8 caracteres" 
            class="input input-bordered w-full" 
            required
          />
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Confirmar contraseña</span>
          </label>
          <input 
            v-model="form.password_confirm" 
            type="password" 
            placeholder="Repite tu contraseña" 
            class="input input-bordered w-full" 
            required
          />
        </div>

        <div class="form-control">
          <label class="cursor-pointer label justify-start">
            <input v-model="form.terms" type="checkbox" class="checkbox checkbox-primary mr-2" />
            <span class="label-text">
              Acepto los <a href="#" class="link link-primary">términos y condiciones</a>
            </span>
          </label>
        </div>

        <div v-if="errors.general" class="alert alert-error">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ errors.general }}</span>
        </div>

        <div class="form-control mt-6">
          <button type="submit" class="btn btn-primary" :disabled="loading || !form.terms">
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Creando cuenta...' : 'Crear Cuenta' }}
          </button>
        </div>
      </form>

      <div class="divider">O</div>

      <div class="text-center">
        <p class="text-sm">
          ¿Ya tienes una cuenta? 
          <router-link :to="{ name: 'Login' }" class="link link-primary">
            Inicia sesión aquí
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: '',
  user_type: 'individual',
  phone: '',
  organization: '',
  terms: false
})

const errors = reactive({
  general: ''
})

const loading = ref(false)

// Watch password confirmation
watch(() => form.password_confirm, (newVal) => {
  if (newVal && form.password && newVal !== form.password) {
    errors.general = 'Las contraseñas no coinciden'
  } else {
    errors.general = ''
  }
})

const handleRegister = async () => {
  if (form.password !== form.password_confirm) {
    errors.general = 'Las contraseñas no coinciden'
    return
  }

  if (form.password.length < 8) {
    errors.general = 'La contraseña debe tener al menos 8 caracteres'
    return
  }

  loading.value = true
  errors.general = ''

  const result = await authStore.register({
    username: form.username,
    email: form.email,
    password: form.password,
    password_confirm: form.password_confirm,
    first_name: form.first_name,
    last_name: form.last_name,
    user_type: form.user_type,
    phone: form.phone || undefined,
    organization: form.organization || undefined
  })

  loading.value = false

  if (result.success) {
    router.push({ name: 'Home' })
  } else {
    errors.general = result.error || 'Error al crear la cuenta'
  }
}
</script>