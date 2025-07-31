<template>
  <div class="min-h-screen">
    <!-- Hero Image Section -->
    <section class="relative h-[500px] w-full overflow-hidden">
      <img 
        src="/hero-1.png" 
        alt="Base43 - Plataforma Web Base" 
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
      <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
        <div class="container-custom mx-auto text-center">
          <h1 class="text-5xl md:text-6xl font-bold mb-4">Quiénes somos</h1>
          <p class="text-xl md:text-2xl">Promotora social e inclusiva</p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="container-custom mx-auto section-padding py-12">
      <div class="max-w-6xl mx-auto">
        <!-- Mission Section -->
        <div class="grid md:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <div class="flex items-center gap-4 mb-6">
              <div class="p-3 bg-primary/10 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h2 class="text-3xl font-bold">Nuestra misión</h2>
            </div>
            <p class="text-lg text-gray-700 mb-4">
              Base43 es una plataforma web moderna y escalable diseñada para servir como base sólida para proyectos web profesionales. Construida con las mejores prácticas de desarrollo, ofrece una arquitectura robusta que combina Django en el backend con Vue.js en el frontend.
            </p>
            <p class="text-lg text-gray-700">
              Nuestra misión es proporcionar una base de código limpia, bien estructurada y fácilmente extensible que permita a los desarrolladores iniciar sus proyectos con una base sólida. Incluimos funcionalidades esenciales como autenticación, gestión de contenido, chat en tiempo real y más.
            </p>
          </div>
          <div class="relative">
            <img 
              src="/pattern-2.png" 
              alt="Base43 - Arquitectura moderna" 
              class="w-full h-auto rounded-lg shadow-lg"
            />
          </div>
        </div>

        <!-- Principles Section -->
        <div class="mb-16">
          <h2 class="text-3xl font-bold text-center mb-12">Principios rectores</h2>
          
          <!-- Principle 1: Accesibilidad y Asequibilidad -->
          <div class="mb-12">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
              <span class="badge badge-primary badge-lg">1</span>
              Accesibilidad y asequibilidad
            </h3>
            <div class="grid md:grid-cols-3 gap-6">
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Diseño universal</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-primary">•</span>
                      <span><strong>Accesibilidad para personas con discapacidad:</strong> Implementar principios de diseño universal para garantizar que las viviendas sean accesibles para personas con discapacidades físicas y sensoriales.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-primary">•</span>
                      <span><strong>Adaptabilidad:</strong> Diseñar viviendas que puedan adaptarse fácilmente a las necesidades cambiantes de los residentes.</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Precios asequibles</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-primary">•</span>
                      <span><strong>Subsidios y ayudas:</strong> Colaborar con gobiernos y organizaciones para ofrecer subsidios o ayudas.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-primary">•</span>
                      <span><strong>Modelos de financiación inclusiva:</strong> Implementar esquemas que consideren las capacidades económicas de diferentes grupos.</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="flex items-center justify-center">
                <div 
                  class="card bg-base-100 shadow-lg cursor-pointer transition-all duration-300 hover:transform hover:-translate-y-1"
                  @click="openImageModal"
                >
                  <figure class="px-4 pt-4">
                    <img 
                      src="/configuracion-cohousing.png" 
                      alt="Configuración Cohousing - Modelo integral de vivienda colaborativa" 
                      class="w-full h-auto rounded-lg"
                    />
                  </figure>
                  <div class="card-body items-center text-center">
                    <p class="text-sm text-gray-600">Click para ampliar</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Principle 2: Participación Comunitaria -->
          <div class="mb-12">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
              <span class="badge badge-secondary badge-lg">2</span>
              Participación comunitaria
            </h3>
            <div class="space-y-6">
              <div class="grid md:grid-cols-2 gap-6">
                <div class="card bg-base-100 shadow-lg">
                  <div class="card-body">
                    <h4 class="font-semibold text-lg mb-3">Involucramiento de la comunidad</h4>
                    <ul class="space-y-2">
                      <li class="flex gap-2">
                        <span class="text-secondary">•</span>
                        <span><strong>Consultas y participación:</strong> Involucrar a los residentes en el proceso de diseño y planificación.</span>
                      </li>
                      <li class="flex gap-2">
                        <span class="text-secondary">•</span>
                        <span><strong>Gobernanza participativa:</strong> Fomentar la creación de comités de residentes.</span>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="card bg-base-100 shadow-lg">
                  <div class="card-body">
                    <h4 class="font-semibold text-lg mb-3">Desarrollo comunitario</h4>
                    <ul class="space-y-2">
                      <li class="flex gap-2">
                        <span class="text-secondary">•</span>
                        <span><strong>Espacios comunes:</strong> Crear espacios que promuevan la interacción y cohesión social.</span>
                      </li>
                      <li class="flex gap-2">
                        <span class="text-secondary">•</span>
                        <span><strong>Programas de apoyo:</strong> Ofrecer servicios de cuidado infantil, actividades para jóvenes y capacitación laboral.</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="flex justify-center">
                <div 
                  class="card bg-base-100 shadow-lg cursor-pointer transition-all duration-300 hover:transform hover:-translate-y-1 max-w-2xl"
                  @click="openStructureModal"
                >
                  <figure class="px-4 pt-4">
                    <img 
                      src="/estructura.png" 
                      alt="Estructura de espacios comunitarios" 
                      class="w-full h-auto rounded-lg"
                    />
                  </figure>
                  <div class="card-body items-center text-center">
                    <p class="text-sm text-gray-600">Click para ampliar</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Principle 3: Diversidad e Inclusión -->
          <div class="mb-12">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
              <span class="badge badge-accent badge-lg">3</span>
              Diversidad e inclusión
            </h3>
            <div class="grid md:grid-cols-2 gap-6">
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Alojamiento de diversas necesidades</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-accent">•</span>
                      <span><strong>Diversidad cultural:</strong> Considerar las necesidades culturales y religiosas de diferentes grupos.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-accent">•</span>
                      <span><strong>Interculturalidad:</strong> Fomentar la convivencia y el respeto entre diferentes culturas.</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Integración social</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-accent">•</span>
                      <span><strong>Inclusión social:</strong> Promover la inclusión de diferentes grupos socioeconómicos.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-accent">•</span>
                      <span><strong>Apoyo a grupos vulnerables:</strong> Implementar políticas específicas para personas sin hogar, refugiados, personas mayores y jóvenes en riesgo.</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- Principle 4: Sostenibilidad y Calidad de Vida -->
          <div class="mb-12">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
              <span class="badge badge-warning badge-lg">4</span>
              Sostenibilidad y calidad de vida
            </h3>
            <div class="grid md:grid-cols-2 gap-6">
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Sostenibilidad ambiental</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-warning">•</span>
                      <span><strong>Construcción sostenible:</strong> Utilizar materiales y técnicas sostenibles para minimizar el impacto ambiental.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-warning">•</span>
                      <span><strong>Eficiencia energética:</strong> Diseñar viviendas energéticamente eficientes.</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="card bg-base-100 shadow-lg">
                <div class="card-body">
                  <h4 class="font-semibold text-lg mb-3">Calidad de vida</h4>
                  <ul class="space-y-2">
                    <li class="flex gap-2">
                      <span class="text-warning">•</span>
                      <span><strong>Servicios básicos:</strong> Asegurar acceso a agua potable, saneamiento, electricidad y conectividad digital.</span>
                    </li>
                    <li class="flex gap-2">
                      <span class="text-warning">•</span>
                      <span><strong>Entorno seguro:</strong> Crear entornos seguros mediante diseño urbano y colaboración con autoridades.</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- Principle 5: Educación y Capacitación Laboral -->
          <div class="mb-12">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
              <span class="badge badge-info badge-lg">5</span>
              Educación y Capacitación Laboral
            </h3>
            <div class="card bg-base-100 shadow-lg">
              <div class="card-body">
                <ul class="space-y-2">
                  <li class="flex gap-2">
                    <span class="text-info">•</span>
                    <span><strong>Programas educativos:</strong> Ofrecer programas educativos y de capacitación laboral para mejorar las oportunidades de empleo y desarrollo personal de los residentes.</span>
                  </li>
                  <li class="flex gap-2">
                    <span class="text-info">•</span>
                    <span><strong>Acceso a recursos:</strong> Facilitar el acceso a recursos educativos, como bibliotecas, centros de formación y apoyo escolar.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Conclusion Section -->
        <div class="card bg-gradient-to-br from-primary/5 to-secondary/5 border-l-4 border-primary mb-16">
          <div class="card-body">
            <h2 class="text-2xl font-bold mb-4">Conclusión</h2>
            <p class="text-lg text-gray-700">
              Implementar estos principios en una promotora de vivienda social no solo mejora la calidad de vida de los residentes, sino que también contribuye a la creación de comunidades más equitativas, inclusivas y resilientes.
            </p>
          </div>
        </div>

        <!-- CTA Section -->
        <div class="card mb-16 relative overflow-hidden">
          <div 
            class="absolute inset-0 opacity-40"
            style="background-image: url('/futuro.png'); background-size: 80%; background-position: center; background-repeat: no-repeat;"
          ></div>
          <div class="absolute inset-0 bg-white/60"></div>
          <div class="card-body text-center py-12 relative z-10">
            <h2 class="card-title text-3xl justify-center mb-4 text-black font-bold">¡Por la vivienda digna!</h2>
            <p class="text-lg mb-8 text-black font-medium">
              Únete a nuestra comunidad y trabajemos juntos por el derecho a una vivienda digna y asequible.
            </p>
            <div class="flex gap-4 justify-center flex-wrap">
              <router-link to="/contacto" class="btn btn-primary shadow-xl font-semibold">
                Solicitar información
              </router-link>
              <router-link to="/proyectos" class="btn btn-outline btn-primary shadow-xl font-semibold">
                Ver proyectos disponibles
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Image Modal -->
    <div v-if="showModal" class="modal modal-open" @click="closeImageModal">
      <div class="modal-box max-w-5xl">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeImageModal">✕</button>
        <figure class="mt-4">
          <img 
            src="/configuracion-cohousing.png" 
            alt="Configuración Cohousing - Modelo integral de vivienda colaborativa" 
            class="w-full h-auto"
          />
        </figure>
      </div>
    </div>

    <!-- Structure Modal -->
    <div v-if="showStructureModal" class="modal modal-open" @click="closeStructureModal">
      <div class="modal-box max-w-5xl">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="closeStructureModal">✕</button>
        <figure class="mt-4">
          <img 
            src="/estructura.png" 
            alt="Estructura de espacios comunitarios" 
            class="w-full h-auto"
          />
        </figure>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

// Modal states
const showModal = ref(false)
const showStructureModal = ref(false)

// Modal functions
const openImageModal = () => {
  showModal.value = true
}

const closeImageModal = () => {
  showModal.value = false
}

const openStructureModal = () => {
  showStructureModal.value = true
}

const closeStructureModal = () => {
  showStructureModal.value = false
}

// Animation on scroll (optional)
onMounted(() => {
  // You can add scroll animations here if needed
})
</script>

<style scoped>
/* Custom animations */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.hero svg {
  animation: float 3s ease-in-out infinite;
}

/* Card hover effects */
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}
</style>