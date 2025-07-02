<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-primary">404</h1>
      <p class="text-2xl font-semibold mt-4">Página no encontrada</p>
      <p class="text-gray-600 mt-2 mb-8">
        Lo sentimos, la página que buscas no existe o ha sido movida.
      </p>
      <div class="space-x-4">
        <router-link :to="{ name: 'Home' }" class="btn btn-primary">
          Volver al inicio
        </router-link>
        <button @click="$router.go(-1)" class="btn btn-outline">
          Ir atrás
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// No specific logic needed for 404 page
</script>