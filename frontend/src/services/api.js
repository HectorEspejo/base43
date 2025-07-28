import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    // Skip interceptor for logout endpoint to avoid loops
    if (originalRequest.url?.includes('/auth/logout/')) {
      return Promise.reject(error)
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // Try to refresh the token
      const refreshed = await authStore.refreshAccessToken()
      if (refreshed) {
        // Update the Authorization header with new token
        originalRequest.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`
        return api(originalRequest)
      } else {
        // Clear tokens without making API call
        authStore.clearSession()
        router.push({ name: 'Login' })
      }
    }

    return Promise.reject(error)
  }
)

export default api