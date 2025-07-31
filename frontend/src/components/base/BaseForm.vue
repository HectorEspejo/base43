<template>
  <form @submit.prevent="handleSubmit" :class="formClass">
    <slot :errors="errors" :isSubmitting="isSubmitting" />
  </form>
</template>

<script setup>
import { ref, provide } from 'vue'

const props = defineProps({
  onSubmit: {
    type: Function,
    required: true
  },
  formClass: {
    type: String,
    default: 'space-y-4'
  },
  validateOnSubmit: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['submit', 'error'])

const errors = ref({})
const isSubmitting = ref(false)

// Provide form state to child components
provide('formErrors', errors)
provide('isSubmitting', isSubmitting)

const setError = (field, message) => {
  errors.value[field] = message
}

const clearError = (field) => {
  delete errors.value[field]
}

const clearAllErrors = () => {
  errors.value = {}
}

const handleSubmit = async () => {
  if (isSubmitting.value) return
  
  isSubmitting.value = true
  clearAllErrors()
  
  try {
    await props.onSubmit()
    emit('submit')
  } catch (error) {
    // Handle validation errors
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else if (error.response?.data?.detail) {
      errors.value = { general: error.response.data.detail }
    } else {
      errors.value = { general: 'An error occurred. Please try again.' }
    }
    emit('error', error)
  } finally {
    isSubmitting.value = false
  }
}

// Expose methods for parent component
defineExpose({
  setError,
  clearError,
  clearAllErrors
})
</script>