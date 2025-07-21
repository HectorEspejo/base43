<template>
  <div class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <nav class="navbar bg-base-100 shadow-md sticky top-0 z-50 min-h-14 sm:min-h-16">
      <div class="navbar-content w-full px-2 sm:px-4 mx-auto max-w-[1400px] flex items-center">
        <!-- Mobile Layout -->
        <div class="xl:hidden flex items-center justify-between w-full relative">
          <!-- Mobile Menu Button (Left) -->
          <div class="relative" ref="mobileMenuDropdown">
            <label tabindex="0" class="btn btn-ghost btn-sm p-1" @click.stop="toggleMobileMenu" @touchstart.stop>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
            </label>
            <ul v-if="showMobileMenu" tabindex="0" class="menu menu-sm absolute left-0 top-full mt-3 z-50 p-2 shadow-lg bg-base-100 rounded-box w-56 sm:w-64 border border-base-200">
              <li class="menu-title px-4 py-2">
                <span class="text-xs uppercase">Navegación</span>
              </li>
              <li><router-link :to="{ name: 'QuienesSomos' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Quiénes somos
              </router-link></li>
              <li><router-link :to="{ name: 'Oferta' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Oferta
              </router-link></li>
              <li><router-link :to="{ name: 'Repositorio' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Repositorio
              </router-link></li>
              <li><router-link :to="{ name: 'Proyectos' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                Proyectos
              </router-link></li>
              <li><router-link :to="{ name: 'Noticias' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                </svg>
                Noticias
              </router-link></li>
              <li><router-link :to="{ name: 'Chat' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
                Chat
              </router-link></li>
              <li><router-link :to="{ name: 'Partners' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Partners
              </router-link></li>
              <li><router-link :to="{ name: 'Contacto' }" class="py-3" @click="closeMobileMenu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Contacto
              </router-link></li>
            </ul>
          </div>
          
          <!-- Logo (Center) -->
          <router-link :to="{ name: 'Home' }" class="btn btn-ghost btn-sm normal-case text-base flex items-center gap-1 px-1 mx-auto">
            <img src="/calicanto-test-logo.png" alt="Calicanto Logo" class="h-5 w-5" />
            <span>Calicanto</span>
          </router-link>
          
          <!-- Auth Buttons (Right) -->
          <div class="flex items-center gap-2">
            <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuDropdown">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar btn-sm" @click.stop="toggleUserMenu" @touchstart.stop>
                <div class="w-8 rounded-full">
                  <img 
                    :src="authStore.currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + authStore.currentUser?.username" 
                    :alt="authStore.currentUser?.username"
                  />
                </div>
              </label>
              <ul v-if="showUserMenu" tabindex="0" class="menu menu-sm absolute right-0 top-full mt-3 z-50 p-2 shadow-lg bg-base-100 rounded-box w-52 border border-base-200">
                <li class="menu-title">
                  <span>{{ authStore.currentUser?.username }}</span>
                </li>
                <li><router-link :to="{ name: 'Profile' }" @click="closeUserMenu">Mi Perfil</router-link></li>
                <li><a @click="handleLogoutAndCloseMenu">Cerrar Sesión</a></li>
              </ul>
            </div>
            <div v-else class="relative" ref="authMenuDropdown">
              <label tabindex="0" class="btn btn-ghost btn-sm btn-circle" @click.stop="toggleAuthMenu" @touchstart.stop>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </label>
              <ul v-if="showAuthMenu" tabindex="0" class="menu menu-sm absolute right-0 top-full mt-3 z-50 p-2 shadow-lg bg-base-100 rounded-box w-52 border border-base-200">
                <li>
                  <router-link :to="{ name: 'Login' }" class="py-3" @click="closeAuthMenu">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Iniciar sesión
                  </router-link>
                </li>
                <li>
                  <router-link :to="{ name: 'Register' }" class="py-3" @click="closeAuthMenu">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    Registrarse
                  </router-link>
                </li>
              </ul>
            </div>
            <!-- Adobe Verde Link -->
            <a href="https://www.adobeverde.es/" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm flex items-center gap-1 px-2">
              <img src="/adobeverde.png" alt="Adobe Verde" class="h-10 w-10 object-contain" />
              <span class="hidden sm:inline">AdobeVerde</span>
            </a>
          </div>
        </div>
        
        <!-- Desktop Layout -->
        <div class="hidden xl:flex items-center w-full justify-between">
          <div class="flex items-center flex-none">
            <router-link :to="{ name: 'Home' }" class="btn btn-ghost btn-sm normal-case text-base flex items-center gap-1 px-1">
              <img src="/calicanto-test-logo.png" alt="Calicanto Logo" class="h-5 w-5" />
              <span>Calicanto</span>
            </router-link>
          </div>
          
          <div class="flex items-center absolute left-1/2 transform -translate-x-1/2">
            <ul class="menu menu-horizontal px-1 items-center gap-0 text-sm">
            <li><router-link :to="{ name: 'QuienesSomos' }" class="px-2">Quiénes somos</router-link></li>
            <li><router-link :to="{ name: 'Oferta' }" class="px-2">Oferta</router-link></li>
            <li><router-link :to="{ name: 'Repositorio' }" class="px-2">Repositorio</router-link></li>
            <li><router-link :to="{ name: 'Proyectos' }" class="px-2">Proyectos</router-link></li>
            <li><router-link :to="{ name: 'Noticias' }" class="px-2">Noticias</router-link></li>
            <li><router-link :to="{ name: 'Chat' }" class="px-2">Chat</router-link></li>
            <li><router-link :to="{ name: 'Partners' }" class="px-2">Partners</router-link></li>
              <li><router-link :to="{ name: 'Contacto' }" class="px-2 mr-12">Contacto</router-link></li>
            </ul>
          </div>
          
          <div class="flex items-center flex-none gap-2">
            <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuDropdownDesktop">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar btn-md" @click.stop="toggleUserMenu" @touchstart.stop>
                <div class="w-10 rounded-full">
                  <img 
                    :src="authStore.currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + authStore.currentUser?.username" 
                    :alt="authStore.currentUser?.username"
                  />
                </div>
              </label>
              <ul v-if="showUserMenu" tabindex="0" class="menu menu-sm absolute right-0 top-full mt-3 z-50 p-2 shadow-lg bg-base-100 rounded-box w-52 border border-base-200">
                <li class="menu-title">
                  <span>{{ authStore.currentUser?.username }}</span>
                </li>
                <li><router-link :to="{ name: 'Profile' }" @click="closeUserMenu">Mi Perfil</router-link></li>
                <li><a @click="handleLogoutAndCloseMenu">Cerrar Sesión</a></li>
              </ul>
            </div>
            <div v-else class="flex items-center gap-2">
              <router-link :to="{ name: 'Login' }" class="btn btn-ghost btn-sm px-4">
                Iniciar sesión
              </router-link>
              <router-link :to="{ name: 'Register' }" class="btn btn-primary btn-sm px-4">
                Registrarse
              </router-link>
              <!-- Adobe Verde Link -->
              <a href="https://www.adobeverde.es/" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm flex items-center gap-1 px-2">
                <img src="/adobeverde.png" alt="Adobe Verde" class="h-8 w-8 object-contain" />
                <span class="text-sm">AdobeVerde</span>
              </a>
            </div>
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
    <footer class="footer footer-center p-6 sm:p-10 bg-base-200 text-base-content">
      <div class="grid grid-flow-col gap-2 sm:gap-4 text-sm sm:text-base">
        <router-link :to="{ name: 'Contacto' }" class="link link-hover">Contacto</router-link>
        <a href="#" class="link link-hover">Términos</a>
        <a href="#" class="link link-hover">Privacidad</a>
      </div>
      <div class="text-center px-4">
        <p class="text-sm sm:text-base">© 2025 Calicanto - Plataforma comunitaria por la vivienda</p>
        <p class="text-xs sm:text-sm mt-1">Licencia Copyleft - Todos los derechos compartidos</p>
        <p class="text-xs sm:text-sm">Con la tecnología de 4d3</p>
      </div>
      <!-- Logos de financiación -->
      <div class="flex items-center justify-center gap-3 sm:gap-6 mt-4 sm:mt-6 px-4 sm:px-0 w-full max-w-full overflow-hidden">
        <img src="/ue.png" alt="Union Europea" class="h-10 sm:h-16 max-w-[80px] sm:max-w-none object-contain flex-shrink-0" />
        <img src="/mites.png" alt="MITES" class="h-10 sm:h-16 max-w-[80px] sm:max-w-none object-contain flex-shrink-0" />
        <img src="/prtr.png" alt="PRTR" class="h-16 sm:h-32 max-w-[120px] sm:max-w-none object-contain flex-shrink-0" />
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Mobile menu state
const showMobileMenu = ref(false)
const mobileMenuDropdown = ref(null)
const showAuthMenu = ref(false)
const authMenuDropdown = ref(null)
const showUserMenu = ref(false)
const userMenuDropdown = ref(null)
const userMenuDropdownDesktop = ref(null)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const toggleAuthMenu = () => {
  showAuthMenu.value = !showAuthMenu.value
}

const closeAuthMenu = () => {
  showAuthMenu.value = false
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

// Click outside handler
const handleClickOutside = (event) => {
  if (mobileMenuDropdown.value && !mobileMenuDropdown.value.contains(event.target)) {
    closeMobileMenu()
  }
  if (authMenuDropdown.value && !authMenuDropdown.value.contains(event.target)) {
    closeAuthMenu()
  }
  if (userMenuDropdown.value && !userMenuDropdown.value.contains(event.target)) {
    closeUserMenu()
  }
  if (userMenuDropdownDesktop.value && !userMenuDropdownDesktop.value.contains(event.target)) {
    closeUserMenu()
  }
}

// Add/remove click listener
onMounted(() => {
  // Add a small delay to prevent immediate closing
  setTimeout(() => {
    document.addEventListener('click', handleClickOutside)
    document.addEventListener('touchstart', handleClickOutside)
  }, 100)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('touchstart', handleClickOutside)
})

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'Home' })
}

const handleLogoutAndCloseMenu = async () => {
  closeUserMenu()
  await handleLogout()
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