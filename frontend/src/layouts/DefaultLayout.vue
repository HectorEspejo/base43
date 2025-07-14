<template>
  <div class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <nav class="navbar bg-base-100 shadow-md sticky top-0 z-50 min-h-16">
      <div class="navbar-content w-full px-4 mx-auto max-w-7xl flex items-center">
        <div class="navbar-start flex items-center flex-none w-auto">
          <div class="dropdown">
            <label tabindex="0" class="btn btn-ghost lg:hidden">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
            </label>
            <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
              <li><router-link :to="{ name: 'QuienesSomos' }">Quiénes somos</router-link></li>
              <li><router-link :to="{ name: 'Oferta' }">Oferta</router-link></li>
              <li><router-link :to="{ name: 'Repositorio' }">Repositorio</router-link></li>
              <li><router-link :to="{ name: 'Proyectos' }">Proyectos</router-link></li>
              <li><router-link :to="{ name: 'Noticias' }">Noticias</router-link></li>
              <li><router-link :to="{ name: 'Chat' }">Chat</router-link></li>
              <li><router-link :to="{ name: 'Partners' }">Partners</router-link></li>
              <li><router-link :to="{ name: 'Contacto' }">Contacto</router-link></li>
            </ul>
          </div>
          <router-link :to="{ name: 'Home' }" class="btn btn-ghost normal-case text-lg flex items-center gap-2 px-2">
            <img src="/calicanto-test-logo.png" alt="Calicanto Logo" class="h-6 w-6" />
            <span class="hidden sm:inline">Calicanto</span>
          </router-link>
        </div>
        
        <div class="navbar-center hidden lg:flex items-center flex-1 justify-center">
          <ul class="menu menu-horizontal px-1 items-center gap-1">
            <li><router-link :to="{ name: 'QuienesSomos' }">Quiénes somos</router-link></li>
            <li><router-link :to="{ name: 'Oferta' }">Oferta</router-link></li>
            <li><router-link :to="{ name: 'Repositorio' }">Repositorio</router-link></li>
            <li><router-link :to="{ name: 'Proyectos' }">Proyectos</router-link></li>
            <li><router-link :to="{ name: 'Noticias' }">Noticias</router-link></li>
            <li><router-link :to="{ name: 'Chat' }">Chat</router-link></li>
            <li><router-link :to="{ name: 'Partners' }">Partners</router-link></li>
            <li><router-link :to="{ name: 'Contacto' }">Contacto</router-link></li>
          </ul>
        </div>
        
        <div class="navbar-end flex items-center flex-none w-auto">
          <div v-if="authStore.isAuthenticated" class="dropdown dropdown-end">
            <label tabindex="0" class="btn btn-ghost btn-circle avatar">
              <div class="w-10 rounded-full">
                <img 
                  :src="authStore.currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + authStore.currentUser?.username" 
                  :alt="authStore.currentUser?.username"
                />
              </div>
            </label>
            <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
              <li class="menu-title">
                <span>{{ authStore.currentUser?.username }}</span>
              </li>
              <li><router-link :to="{ name: 'Profile' }">Mi Perfil</router-link></li>
              <li><a @click="handleLogout">Cerrar Sesión</a></li>
            </ul>
          </div>
          <div v-else class="flex items-center gap-2">
            <router-link :to="{ name: 'Login' }" class="btn btn-ghost btn-sm">
              Iniciar sesión
            </router-link>
            <router-link :to="{ name: 'Register' }" class="btn btn-primary btn-sm">
              Registrarse
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="footer footer-center p-10 bg-base-200 text-base-content">
      <div class="grid grid-flow-col gap-4">
        <router-link :to="{ name: 'Contacto' }" class="link link-hover">Contacto</router-link>
        <a href="#" class="link link-hover">Términos</a>
        <a href="#" class="link link-hover">Privacidad</a>
      </div>
      <div>
        <p>© 2025 Calicanto - Plataforma comunitaria por la vivienda</p>
        <p class="text-sm mt-1">Licencia Copyleft - Todos los derechos compartidos</p>
        <p>Con la tecnología de 4d3</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'Home' })
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>