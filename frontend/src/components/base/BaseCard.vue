<template>
  <div 
    :class="[
      'card bg-base-100',
      shadow && 'shadow-xl',
      hover && 'card-hover transition-all duration-300',
      customClass
    ]"
  >
    <figure v-if="$slots.image || image" :class="imageClass">
      <slot name="image">
        <img v-if="image" :src="image" :alt="imageAlt || title" class="w-full h-full object-cover" />
      </slot>
    </figure>
    
    <div class="card-body" :class="bodyClass">
      <h2 v-if="title" class="card-title" :class="titleClass">
        {{ title }}
        <slot name="badge" />
      </h2>
      
      <slot>
        <p v-if="description">{{ description }}</p>
      </slot>
      
      <div v-if="$slots.actions" class="card-actions" :class="actionsClass">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
  image: String,
  imageAlt: String,
  shadow: {
    type: Boolean,
    default: true
  },
  hover: {
    type: Boolean,
    default: false
  },
  customClass: {
    type: String,
    default: ''
  },
  imageClass: {
    type: String,
    default: ''
  },
  bodyClass: {
    type: String,
    default: ''
  },
  titleClass: {
    type: String,
    default: ''
  },
  actionsClass: {
    type: String,
    default: 'justify-end'
  }
})
</script>

<style scoped>
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
</style>