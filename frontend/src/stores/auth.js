import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

// Create a separate axios instance for auth endpoints to avoid interceptor loops
const authApi = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Actions
  async function login(credentials) {
    loading.value = true
    try {
      const response = await authApi.post('/auth/login/', credentials)
      const { access, refresh, user: userData } = response.data
      
      setTokens(access, refresh)
      user.value = userData
      
      toast.success('Inicio de sesión exitoso')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.error || error.response?.data?.detail || 'Error al iniciar sesión'
      toast.error(message)
      return { success: false, error: message, isVerificationError: error.response?.status === 403 }
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    try {
      const response = await authApi.post('/auth/register/', userData)
      const { message } = response.data
      
      // Ya no recibimos tokens porque el usuario necesita ser verificado
      toast.success(message || 'Registro exitoso. Su cuenta está pendiente de verificación.')
      return { success: true, needsVerification: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Error al registrar usuario'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (refreshToken.value) {
        // Add authorization header for logout
        const config = {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        }
        await authApi.post('/auth/logout/', { refresh_token: refreshToken.value }, config)
      }
    } catch (error) {
      console.error('Error during logout:', error)
    } finally {
      clearTokens()
      user.value = null
      toast.info('Sesión cerrada')
    }
  }

  async function fetchUser() {
    if (!token.value) return
    
    try {
      const response = await api.get('/auth/me/')
      user.value = response.data
    } catch (error) {
      console.error('Error fetching user:', error)
      if (error.response?.status === 401) {
        clearTokens()
      }
    }
  }

  async function updateProfile(profileData) {
    loading.value = true
    try {
      const response = await api.patch('/auth/profile/', profileData)
      user.value = { ...user.value, ...response.data }
      toast.success('Perfil actualizado correctamente')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Error al actualizar perfil'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  async function changePassword(passwordData) {
    loading.value = true
    try {
      await api.put('/auth/change-password/', passwordData)
      toast.success('Contraseña actualizada correctamente')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Error al cambiar contraseña'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  async function uploadAvatar(file) {
    loading.value = true
    try {
      const formData = new FormData()
      formData.append('avatar', file)
      
      const response = await api.patch('/auth/avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response.data.avatar) {
        user.value = { ...user.value, avatar: response.data.avatar }
      }
      
      toast.success('Avatar actualizado correctamente')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.error || 'Error al subir avatar'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) return false
    
    try {
      const response = await authApi.post('/auth/refresh/', {
        refresh: refreshToken.value
      })
      token.value = response.data.access
      localStorage.setItem('access_token', response.data.access)
      return true
    } catch (error) {
      // Token refresh failed, clear everything
      clearTokens()
      user.value = null
      return false
    }
  }

  async function checkAuth() {
    if (token.value && !user.value) {
      await fetchUser()
    }
  }

  // Helper functions
  function setTokens(accessToken, refreshTokenValue) {
    token.value = accessToken
    refreshToken.value = refreshTokenValue
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshTokenValue)
  }

  function clearTokens() {
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  function clearSession() {
    clearTokens()
    user.value = null
  }

  return {
    // State
    user,
    token,
    loading,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    login,
    register,
    logout,
    fetchUser,
    updateProfile,
    changePassword,
    uploadAvatar,
    refreshAccessToken,
    checkAuth,
    clearSession,
  }
})