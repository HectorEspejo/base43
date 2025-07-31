<template>
  <component
    :is="to ? 'router-link' : href ? 'a' : 'button'"
    :to="to"
    :href="href"
    :type="!to && !href ? type : undefined"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <span v-if="loading" class="loading loading-spinner loading-sm"></span>
    <slot v-else>
      {{ label }}
    </slot>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'accent', 'ghost', 'link', 'outline', 'error', 'success', 'warning', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg'].includes(value)
  },
  type: {
    type: String,
    default: 'button'
  },
  to: [String, Object],
  href: String,
  disabled: Boolean,
  loading: Boolean,
  block: Boolean,
  circle: Boolean,
  square: Boolean,
  customClass: String
})

const emit = defineEmits(['click'])

const buttonClasses = computed(() => {
  const classes = ['btn']
  
  // Variant
  if (props.variant === 'outline') {
    classes.push('btn-outline')
  } else if (props.variant !== 'primary') {
    classes.push(`btn-${props.variant}`)
  }
  
  // Size
  classes.push(`btn-${props.size}`)
  
  // Shape
  if (props.circle) classes.push('btn-circle')
  if (props.square) classes.push('btn-square')
  
  // Width
  if (props.block) classes.push('btn-block')
  
  // Loading state
  if (props.loading) classes.push('loading')
  
  // Custom classes
  if (props.customClass) classes.push(props.customClass)
  
  return classes.join(' ')
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>