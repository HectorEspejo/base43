<template>
  <div class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <nav class="navbar bg-white/95 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-gray-100">
      <div class="navbar-content w-full px-4 sm:px-6 mx-auto max-w-7xl">
        <!-- Mobile Layout -->
        <div class="xl:hidden flex items-center justify-between w-full h-16">
          <!-- Mobile Menu Button -->
          <div class="relative" ref="mobileMenuDropdown">
            <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors" @click.stop="toggleMobileMenu" @touchstart.stop>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            <!-- Mobile Menu Dropdown -->
            <ul v-if="showMobileMenu" class="absolute left-0 top-full mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-100 py-2 z-50">
              <li>
                <router-link :to="{ name: 'QuienesSomos' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <span class="font-medium">Quiénes somos</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Oferta' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span class="font-medium">Oferta</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Repositorio' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span class="font-medium">Repositorio</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Recursos' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="font-medium">Recursos</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Proyectos' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span class="font-medium">Proyectos</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Noticias' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                  </svg>
                  <span class="font-medium">Noticias</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Chat' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                  </svg>
                  <span class="font-medium">Chat</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Partners' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <span class="font-medium">Partners</span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'Contacto' }" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeMobileMenu">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span class="font-medium">Contacto</span>
                </router-link>
              </li>
            </ul>
          </div>
          
          <!-- Logo (Center) -->
          <router-link :to="{ name: 'Home' }" class="flex items-center">
            <img src="/logo.png" alt="Base43" class="h-14 object-contain" />
          </router-link>
          
          <!-- Right Section -->
          <div class="flex items-center gap-2">
            <!-- Auth Section -->
            <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuDropdown">
              <button class="w-8 h-8 rounded-full overflow-hidden bg-gray-200" @click.stop="toggleUserMenu" @touchstart.stop>
                <img 
                  :src="authStore.currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + authStore.currentUser?.username" 
                  :alt="authStore.currentUser?.username"
                  class="w-full h-full object-cover"
                />
              </button>
              <ul v-if="showUserMenu" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-50">
                <li class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm font-medium">{{ authStore.currentUser?.username }}</p>
                </li>
                <li>
                  <router-link :to="{ name: 'Profile' }" @click="closeUserMenu" class="block px-4 py-2 hover:bg-gray-50 transition-colors">
                    Mi Perfil
                  </router-link>
                </li>
                <li>
                  <button @click="handleLogoutAndCloseMenu" class="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors text-red-600">
                    Cerrar Sesión
                  </button>
                </li>
              </ul>
            </div>
            <div v-else class="relative" ref="authMenuDropdown">
              <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors" @click.stop="toggleAuthMenu" @touchstart.stop>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </button>
              <ul v-if="showAuthMenu" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-50">
                <li>
                  <router-link :to="{ name: 'Login' }" class="flex items-center gap-2 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeAuthMenu">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    <span>Iniciar sesión</span>
                  </router-link>
                </li>
                <li>
                  <router-link :to="{ name: 'Register' }" class="flex items-center gap-2 px-4 py-3 hover:bg-gray-50 transition-colors" @click="closeAuthMenu">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    <span>Registrarse</span>
                  </router-link>
                </li>
              </ul>
            </div>
            
            <!-- Adobe Verde Link -->
            <a href="https://www.adobeverde.es/" target="_blank" rel="noopener noreferrer" class="flex items-center">
              <img src="/adobeverde.png" alt="Adobe Verde" class="h-8 object-contain" />
            </a>
          </div>
        </div>
        
        <!-- Desktop Layout -->
        <div class="hidden xl:flex items-center justify-between w-full h-20">
          <!-- Logo (Left) -->
          <div class="flex items-center flex-shrink-0">
            <router-link :to="{ name: 'Home' }" class="flex items-center">
              <img src="/logo.png" alt="Base43" class="h-20 object-contain" />
            </router-link>
          </div>
          
          <!-- Navigation Menu (Center) -->
          <nav class="flex items-center flex-1 justify-center px-4">
            <ul class="menu menu-horizontal p-0 items-center gap-0 whitespace-nowrap">
              <li><router-link :to="{ name: 'QuienesSomos' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Quiénes somos</router-link></li>
              <li><router-link :to="{ name: 'Oferta' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Oferta</router-link></li>
              <li><router-link :to="{ name: 'Repositorio' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Repositorio</router-link></li>
              <li><router-link :to="{ name: 'Recursos' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Recursos</router-link></li>
              <li><router-link :to="{ name: 'Proyectos' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Proyectos</router-link></li>
              <li><router-link :to="{ name: 'Noticias' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Noticias</router-link></li>
              <li><router-link :to="{ name: 'Chat' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Chat</router-link></li>
              <li><router-link :to="{ name: 'Partners' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Partners</router-link></li>
              <li><router-link :to="{ name: 'Contacto' }" class="px-1.5 py-2 text-xs font-medium hover:text-primary transition-colors">Contacto</router-link></li>
            </ul>
          </nav>
          
          <!-- Auth Section (Right) -->
          <div class="flex items-center gap-2 flex-shrink-0 justify-end">
            <!-- Authenticated User -->
            <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuDropdownDesktop">
              <button class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors" @click.stop="toggleUserMenu">
                <div class="w-8 h-8 rounded-full overflow-hidden bg-gray-200">
                  <img 
                    :src="authStore.currentUser?.avatar || 'https://ui-avatars.com/api/?name=' + authStore.currentUser?.username" 
                    :alt="authStore.currentUser?.username"
                    class="w-full h-full object-cover"
                  />
                </div>
                <span class="font-medium text-gray-700">{{ authStore.currentUser?.username }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <ul v-if="showUserMenu" class="absolute right-0 top-full mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-50">
                <li class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm text-gray-500">Conectado como</p>
                  <p class="font-medium">{{ authStore.currentUser?.email }}</p>
                </li>
                <li>
                  <router-link :to="{ name: 'Profile' }" @click="closeUserMenu" class="block px-4 py-2 hover:bg-gray-50 transition-colors">
                    <div class="flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span>Mi Perfil</span>
                    </div>
                  </router-link>
                </li>
                <li>
                  <button @click="handleLogoutAndCloseMenu" class="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors text-red-600">
                    <div class="flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      <span>Cerrar Sesión</span>
                    </div>
                  </button>
                </li>
              </ul>
            </div>
            
            <!-- Guest User -->
            <div v-else class="flex items-center gap-3">
              <router-link :to="{ name: 'Login' }" class="px-4 py-2 text-gray-700 font-medium hover:text-primary transition-colors mr-2">
                Iniciar sesión
              </router-link>
              <router-link :to="{ name: 'Register' }" class="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-primary-focus transition-colors">
                Registrarse
              </router-link>
            </div>
          </div>
          
          <!-- Adobe Verde Link (Far Right) -->
          <a href="https://www.adobeverde.es/" target="_blank" rel="noopener noreferrer" class="ml-6 flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors flex-shrink-0">
            <img src="/adobeverde.png" alt="Adobe Verde" class="h-8 object-contain" />
            <span class="text-sm font-medium text-gray-700">AdobeVerde</span>
          </a>
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
        <router-link :to="{ name: 'Terminos' }" class="link link-hover">Términos</router-link>
        <router-link :to="{ name: 'Privacidad' }" class="link link-hover">Privacidad</router-link>
      </div>
      <div class="text-center px-4">
        <p class="text-sm sm:text-base">© 2025 Base43 - Plataforma Web Base</p>
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

/* Active route styling */
.router-link-active {
  color: var(--primary);
}

/* Smooth scrollbar for mobile menu */
ul::-webkit-scrollbar {
  width: 4px;
}

ul::-webkit-scrollbar-track {
  background: #f1f1f1;
}

ul::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 2px;
}

ul::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>