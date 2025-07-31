<template>
  <Teleport to="body">
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="modelValue" class="modal modal-open" @click="handleBackdropClick">
        <div 
          class="modal-box"
          :class="[sizeClass, customClass]"
          @click.stop
        >
          <!-- Header -->
          <div v-if="title || $slots.header" class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-lg">
              <slot name="header">{{ title }}</slot>
            </h3>
            <button
              v-if="closable"
              type="button"
              class="btn btn-sm btn-circle btn-ghost"
              @click="close"
            >
              ✕
            </button>
          </div>
          
          <!-- Body -->
          <div class="modal-body">
            <slot />
          </div>
          
          <!-- Actions -->
          <div v-if="$slots.actions" class="modal-action">
            <slot name="actions" :close="close" />
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: String,
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  closeOnEsc: {
    type: Boolean,
    default: true
  },
  customClass: String
})

const emit = defineEmits(['update:modelValue', 'close', 'open'])

const sizeClass = computed(() => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full mx-4'
  }
  return sizes[props.size] || sizes.md
})

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleBackdropClick = () => {
  if (props.closeOnBackdrop && props.closable) {
    close()
  }
}

const handleEscKey = (event) => {
  if (event.key === 'Escape' && props.closeOnEsc && props.closable && props.modelValue) {
    close()
  }
}

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    emit('open')
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
  document.body.style.overflow = ''
})
</script>