<template>
  <div class="container-custom mx-auto section-padding py-8">
    <h1 class="text-4xl font-bold mb-8">Mi Perfil</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Profile Sidebar -->
      <div class="lg:col-span-1">
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body items-center text-center">
            <div class="avatar mb-4">
              <div class="w-32 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img 
                  :src="user?.avatar || 'https://ui-avatars.com/api/?name=' + user?.username" 
                  :alt="user?.username"
                />
              </div>
            </div>
            <h2 class="card-title">{{ user?.first_name }} {{ user?.last_name }}</h2>
            <p class="text-gray-600">@{{ user?.username }}</p>
            <div class="badge badge-primary">{{ getUserTypeLabel(user?.user_type) }}</div>
            
            <div class="divider"></div>
            
            <div class="w-full space-y-2 text-left">
              <p class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                {{ user?.email }}
              </p>
              <p v-if="user?.phone" class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                {{ user?.phone }}
              </p>
              <p v-if="user?.organization" class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                {{ user?.organization }}
              </p>
            </div>
            
            <div class="card-actions justify-center mt-6">
              <label for="avatar-upload" class="btn btn-outline btn-sm">
                Cambiar avatar
                <input 
                  id="avatar-upload" 
                  type="file" 
                  accept="image/*" 
                  class="hidden"
                  @change="handleAvatarChange"
                />
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Content -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Personal Information -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title mb-4">Información Personal</h2>
            
            <form @submit.prevent="updateProfile" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Nombre</span>
                  </label>
                  <input 
                    v-model="profileForm.first_name" 
                    type="text" 
                    class="input input-bordered" 
                    required
                  />
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Apellidos</span>
                  </label>
                  <input 
                    v-model="profileForm.last_name" 
                    type="text" 
                    class="input input-bordered" 
                    required
                  />
                </div>
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text">Teléfono</span>
                </label>
                <input 
                  v-model="profileForm.phone" 
                  type="tel" 
                  class="input input-bordered" 
                  placeholder="+34 600 000 000"
                />
              </div>

              <div v-if="user?.user_type !== 'individual'" class="form-control">
                <label class="label">
                  <span class="label-text">Organización</span>
                </label>
                <input 
                  v-model="profileForm.organization" 
                  type="text" 
                  class="input input-bordered" 
                />
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text">Biografía</span>
                </label>
                <textarea 
                  v-model="profileForm.bio" 
                  class="textarea textarea-bordered h-24" 
                  placeholder="Cuéntanos sobre ti..."
                ></textarea>
              </div>

              <div class="card-actions justify-end">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="loading loading-spinner"></span>
                  {{ loading ? 'Guardando...' : 'Guardar cambios' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Change Password -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title mb-4">Cambiar Contraseña</h2>
            
            <form @submit.prevent="changePassword" class="space-y-4">
              <div class="form-control">
                <label class="label">
                  <span class="label-text">Contraseña actual</span>
                </label>
                <input 
                  v-model="passwordForm.old_password" 
                  type="password" 
                  class="input input-bordered" 
                  required
                />
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text">Nueva contraseña</span>
                </label>
                <input 
                  v-model="passwordForm.new_password" 
                  type="password" 
                  class="input input-bordered" 
                  required
                />
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text">Confirmar nueva contraseña</span>
                </label>
                <input 
                  v-model="passwordForm.confirm_password" 
                  type="password" 
                  class="input input-bordered" 
                  required
                />
              </div>

              <div class="card-actions justify-end">
                <button type="submit" class="btn btn-primary" :disabled="passwordLoading">
                  <span v-if="passwordLoading" class="loading loading-spinner"></span>
                  {{ passwordLoading ? 'Cambiando...' : 'Cambiar contraseña' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Account Settings -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title mb-4">Configuración de Cuenta</h2>
            
            <div class="space-y-4">
              <div class="form-control">
                <label class="label cursor-pointer">
                  <span class="label-text">Recibir notificaciones por email</span>
                  <input type="checkbox" class="toggle toggle-primary" checked />
                </label>
              </div>
              
              <div class="form-control">
                <label class="label cursor-pointer">
                  <span class="label-text">Perfil público</span>
                  <input type="checkbox" class="toggle toggle-primary" />
                </label>
              </div>
              
              <div class="form-control">
                <label class="label cursor-pointer">
                  <span class="label-text">Modo oscuro</span>
                  <input type="checkbox" class="toggle toggle-primary" />
                </label>
              </div>
            </div>
            
            <div class="divider"></div>
            
            <div class="card-actions justify-between">
              <button class="btn btn-error btn-outline btn-sm">
                Eliminar cuenta
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const toast = useToast()

const user = ref(authStore.currentUser)
const loading = ref(false)
const passwordLoading = ref(false)

const profileForm = reactive({
  first_name: '',
  last_name: '',
  phone: '',
  organization: '',
  bio: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

onMounted(() => {
  if (user.value) {
    profileForm.first_name = user.value.first_name || ''
    profileForm.last_name = user.value.last_name || ''
    profileForm.phone = user.value.phone || ''
    profileForm.organization = user.value.organization || ''
    profileForm.bio = user.value.bio || ''
  }
})

const getUserTypeLabel = (type) => {
  const labels = {
    individual: 'Individual',
    organization: 'Organización',
    partner: 'Partner'
  }
  return labels[type] || type
}

const updateProfile = async () => {
  loading.value = true
  const result = await authStore.updateProfile(profileForm)
  loading.value = false
  
  if (result.success) {
    user.value = authStore.currentUser
  }
}

const changePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.error('Las contraseñas no coinciden')
    return
  }
  
  passwordLoading.value = true
  const result = await authStore.changePassword({
    old_password: passwordForm.old_password,
    new_password: passwordForm.new_password
  })
  passwordLoading.value = false
  
  if (result.success) {
    // Clear form
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  }
}

const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // TODO: Implement avatar upload
    toast.info('Subida de avatar - Próximamente')
  }
}
</script>