<template>
  <div>
    <!-- Hero Section -->
    <section class="hero min-h-[600px] relative">
      <div class="absolute inset-0 z-0">
        <img src="/cooperativa.jpg" alt="Cooperativa Background" class="w-full h-full object-cover" />
        <div class="absolute inset-0 bg-black bg-opacity-50"></div>
      </div>
      <div class="hero-content text-center text-white relative z-10">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-bold mb-6">
            Construyendo lo común. Creando habitabilidad
          </h1>
          <p class="text-xl mb-8">
            Calicanto es una cooperativa de vivienda que conecta personas, proyectos y recursos 
            para crear soluciones de vivienda colaborativa y sostenible.
          </p>
          <div class="space-x-4">
            <router-link :to="{ name: 'Proyectos' }" class="btn btn-secondary btn-lg">
              Ver proyectos
            </router-link>
            <router-link :to="{ name: 'Register' }" class="btn btn-outline btn-lg text-white border-white hover:bg-white hover:text-primary-600">
              Únete a la comunidad
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 section-padding">
      <div class="container-custom">
        <h2 class="text-4xl font-bold text-center mb-12">
          ¿Qué ofrecemos?
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Oferta -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="card-title">Catálogo de servicios</h3>
              <p>Encuentra profesionales y servicios especializados en vivienda colaborativa y construcción sostenible.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Oferta' }" class="btn btn-primary btn-sm">
                  Explorar
                </router-link>
              </div>
            </div>
          </div>

          <!-- Repositorio -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-secondary-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-secondary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="card-title">Documentación libre</h3>
              <p>Accede a recursos, guías y documentación bajo licencias Copyleft para proyectos de vivienda.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Repositorio' }" class="btn btn-secondary btn-sm">
                  Acceder
                </router-link>
              </div>
            </div>
          </div>

          <!-- Proyectos -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-accent bg-opacity-20 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 class="card-title">Proyectos activos</h3>
              <p>Conoce iniciativas de cohousing, centros de menores y otros proyectos de vivienda comunitaria.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Proyectos' }" class="btn btn-accent btn-sm">
                  Ver Proyectos
                </router-link>
              </div>
            </div>
          </div>

          <!-- Chat -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-info bg-opacity-20 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <h3 class="card-title">Chat comunitario</h3>
              <p>Conéctate con otros miembros, comparte experiencias y colabora en tiempo real.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Chat' }" class="btn btn-info btn-sm">
                  Chatear
                </router-link>
              </div>
            </div>
          </div>

          <!-- Noticias -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-success bg-opacity-20 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                </svg>
              </div>
              <h3 class="card-title">Últimas noticias</h3>
              <p>Mantente informado sobre novedades, eventos y actualizaciones de la comunidad.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Noticias' }" class="btn btn-success btn-sm">
                  Leer Más
                </router-link>
              </div>
            </div>
          </div>

          <!-- Partners -->
          <div class="card bg-base-100 shadow-xl card-hover">
            <div class="card-body">
              <div class="w-16 h-16 bg-warning bg-opacity-20 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 class="card-title">Nuestros partners</h3>
              <p>Conoce a las organizaciones que colaboran con nosotros en la construcción de alternativas.</p>
              <div class="card-actions justify-end mt-4">
                <router-link :to="{ name: 'Partners' }" class="btn btn-warning btn-sm">
                  Conocer
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-base-200">
      <div class="container-custom text-center">
        <h2 class="text-4xl font-bold mb-6">
          ¿Listo para formar parte del cambio?
        </h2>
        <p class="text-xl mb-8 max-w-2xl mx-auto">
          Únete a Calicanto y sé parte de una comunidad que está transformando 
          la forma de entender y construir vivienda.
        </p>
        <router-link :to="{ name: 'Contacto' }" class="btn btn-primary btn-lg">
          Contáctanos
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
// Home page doesn't need specific logic for now
</script>