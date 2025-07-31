<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50">
    <div class="mb-8">
      <router-link :to="{ name: 'Home' }" class="text-4xl font-bold text-primary-600">
        Base43
      </router-link>
      <p class="text-center text-gray-600 mt-2">Plataforma Web Base</p>
    </div>
    
    <div class="w-full max-w-md">
      <router-view />
    </div>
    
    <div class="mt-8 text-center text-sm text-gray-600">
      <p>© 2025 Base43 - Todos los derechos reservados</p>
    </div>
  </div>
</template>

<script setup>
// Auth layout doesn't need any specific logic
</script>