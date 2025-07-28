import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layouts
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

// Views
import Home from '@/views/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Oferta from '@/views/Oferta.vue'
import Repositorio from '@/views/Repositorio.vue'
import Proyectos from '@/views/Proyectos.vue'
import Noticias from '@/views/Noticias.vue'
import NewsDetail from '@/views/NewsDetail.vue'
import Chat from '@/views/Chat.vue'
import Partners from '@/views/Partners.vue'
import Contacto from '@/views/Contacto.vue'
import Profile from '@/views/Profile.vue'
import NotFound from '@/views/NotFound.vue'
import QuienesSomos from '@/views/QuienesSomos.vue'
import Recursos from '@/views/Recursos.vue'
import Terminos from '@/views/legal/Terminos.vue'
import Privacidad from '@/views/legal/Privacidad.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: Home,
      },
      {
        path: 'oferta',
        name: 'Oferta',
        component: Oferta,
      },
      {
        path: 'quienes-somos',
        name: 'QuienesSomos',
        component: QuienesSomos,
      },
      {
        path: 'repositorio',
        name: 'Repositorio',
        component: Repositorio,
        meta: { requiresAuth: true },
      },
      {
        path: 'recursos',
        name: 'Recursos',
        component: Recursos,
      },
      {
        path: 'proyectos',
        name: 'Proyectos',
        component: Proyectos,
      },
      {
        path: 'noticias',
        name: 'Noticias',
        component: Noticias,
      },
      {
        path: 'noticias/:year/:month/:day/:slug',
        name: 'NewsDetail',
        component: NewsDetail,
      },
      {
        path: 'chat',
        name: 'Chat',
        component: Chat,
        meta: { requiresAuth: true },
      },
      {
        path: 'partners',
        name: 'Partners',
        component: Partners,
      },
      {
        path: 'contacto',
        name: 'Contacto',
        component: Contacto,
      },
      {
        path: 'perfil',
        name: 'Profile',
        component: Profile,
        meta: { requiresAuth: true },
      },
      {
        path: 'terminos',
        name: 'Terminos',
        component: Terminos,
      },
      {
        path: 'privacidad',
        name: 'Privacidad',
        component: Privacidad,
      },
    ],
  },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { guest: true },
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { guest: true },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router