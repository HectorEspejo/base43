import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()

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
      const response = await api.post('/auth/login/', credentials)
      const { access, refresh, user: userData } = response.data
      
      setTokens(access, refresh)
      user.value = userData
      
      toast.success('Inicio de sesión exitoso')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Error al iniciar sesión'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    try {
      const response = await api.post('/auth/register/', userData)
      const { tokens, user: newUser } = response.data
      
      setTokens(tokens.access, tokens.refresh)
      user.value = newUser
      
      toast.success('Registro exitoso. ¡Bienvenido!')
      return { success: true }
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
        await api.post('/auth/logout/', { refresh_token: refreshToken.value })
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

  async function refreshAccessToken() {
    if (!refreshToken.value) return false
    
    try {
      const response = await api.post('/auth/refresh/', {
        refresh: refreshToken.value
      })
      token.value = response.data.access
      localStorage.setItem('access_token', response.data.access)
      return true
    } catch (error) {
      clearTokens()
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
    refreshAccessToken,
    checkAuth,
  }
})