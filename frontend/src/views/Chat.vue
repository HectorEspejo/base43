<template>
  <div class="flex h-[calc(100vh-4rem)]">
    <!-- Sidebar with channels -->
    <div class="w-64 bg-base-200 p-4 overflow-y-auto">
      <h2 class="text-lg font-bold mb-4">Canales</h2>
      <ul class="menu menu-compact">
        <li v-for="channel in channels" :key="channel.id">
          <a 
            @click="selectChannel(channel)"
            :class="{ 'active': selectedChannel?.id === channel.id }"
          >
            <span class="text-xl mr-2">#</span>
            {{ channel.name }}
            <span v-if="channel.unread" class="badge badge-primary badge-sm ml-auto">
              {{ channel.unread }}
            </span>
          </a>
        </li>
      </ul>
      
      <div class="divider"></div>
      
      <h3 class="text-sm font-semibold mb-2 px-2">Mensajes Directos</h3>
      <ul class="menu menu-compact">
        <li v-for="user in directMessages" :key="user.id">
          <a @click="selectDirectMessage(user)">
            <div class="avatar avatar-xs">
              <div class="w-6 rounded-full">
                <img :src="user.avatar || 'https://ui-avatars.com/api/?name=' + user.name" />
              </div>
            </div>
            {{ user.name }}
            <span v-if="user.online" class="badge badge-success badge-xs ml-auto"></span>
          </a>
        </li>
      </ul>
    </div>

    <!-- Main chat area -->
    <div class="flex-1 flex flex-col">
      <!-- Chat header -->
      <div class="bg-base-100 border-b px-6 py-4">
        <h3 class="text-xl font-semibold">
          {{ selectedChannel ? '#' + selectedChannel.name : 'Selecciona un canal' }}
        </h3>
        <p class="text-sm text-gray-600">
          {{ selectedChannel?.description }}
        </p>
      </div>

      <!-- Messages area -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4" ref="messagesContainer">
        <div v-if="!selectedChannel" class="text-center text-gray-500 mt-20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p>Selecciona un canal para comenzar a chatear</p>
        </div>

        <div v-else v-for="message in messages" :key="message.id" class="chat" :class="message.userId === currentUserId ? 'chat-end' : 'chat-start'">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img :src="message.userAvatar || 'https://ui-avatars.com/api/?name=' + message.userName" />
            </div>
          </div>
          <div class="chat-header">
            {{ message.userName }}
            <time class="text-xs opacity-50 ml-2">{{ formatTime(message.timestamp) }}</time>
          </div>
          <div class="chat-bubble" :class="message.userId === currentUserId ? 'chat-bubble-primary' : ''">
            {{ message.content }}
          </div>
        </div>
      </div>

      <!-- Message input -->
      <div v-if="selectedChannel" class="border-t p-4">
        <form @submit.prevent="sendMessage" class="flex gap-2">
          <input 
            v-model="newMessage"
            type="text" 
            placeholder="Escribe un mensaje..." 
            class="input input-bordered flex-1"
            :disabled="!connected"
          />
          <button type="submit" class="btn btn-primary" :disabled="!newMessage.trim() || !connected">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </div>
    </div>

    <!-- Online users sidebar -->
    <div class="w-64 bg-base-200 p-4 overflow-y-auto border-l">
      <h3 class="text-lg font-bold mb-4">Usuarios Online</h3>
      <ul class="space-y-2">
        <li v-for="user in onlineUsers" :key="user.id" class="flex items-center gap-2">
          <div class="avatar online">
            <div class="w-8 rounded-full">
              <img :src="user.avatar || 'https://ui-avatars.com/api/?name=' + user.name" />
            </div>
          </div>
          <span class="text-sm">{{ user.name }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const toast = useToast()

const currentUserId = ref(authStore.currentUser?.id || 1)
const selectedChannel = ref(null)
const messages = ref([])
const newMessage = ref('')
const connected = ref(false)
const messagesContainer = ref(null)

// Mock data - replace with real data
const channels = ref([
  { id: 1, name: 'general', description: 'Canal general para todos los miembros', unread: 0 },
  { id: 2, name: 'proyectos', description: 'Discusión sobre proyectos activos', unread: 3 },
  { id: 3, name: 'recursos', description: 'Compartir recursos y documentos', unread: 0 },
  { id: 4, name: 'eventos', description: 'Información sobre eventos y talleres', unread: 1 }
])

const directMessages = ref([
  { id: 1, name: 'Ana García', online: true },
  { id: 2, name: 'Carlos López', online: false },
  { id: 3, name: 'María Rodríguez', online: true }
])

const onlineUsers = ref([
  { id: 1, name: 'Ana García', avatar: null },
  { id: 3, name: 'María Rodríguez', avatar: null },
  { id: 4, name: 'Pedro Martín', avatar: null }
])

// Mock messages
const mockMessages = [
  { id: 1, userId: 2, userName: 'Ana García', content: '¡Hola a todos! ¿Cómo va el proyecto?', timestamp: new Date() },
  { id: 2, userId: 1, userName: 'Tú', content: '¡Hola Ana! Todo va muy bien, estamos avanzando con los planos', timestamp: new Date() },
  { id: 3, userId: 3, userName: 'María Rodríguez', content: 'Genial! ¿Cuándo podemos vernos para revisar los detalles?', timestamp: new Date() }
]

const selectChannel = (channel) => {
  selectedChannel.value = channel
  channel.unread = 0
  // Load messages for this channel
  messages.value = [...mockMessages]
  scrollToBottom()
}

const selectDirectMessage = (user) => {
  // TODO: Implement direct messages
  toast.info(`Chat directo con ${user.name} - Próximamente`)
}

const sendMessage = () => {
  if (!newMessage.value.trim() || !connected.value) return

  const message = {
    id: messages.value.length + 1,
    userId: currentUserId.value,
    userName: 'Tú',
    content: newMessage.value,
    timestamp: new Date()
  }

  messages.value.push(message)
  newMessage.value = ''
  
  // TODO: Send message via WebSocket
  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  // TODO: Connect to WebSocket
  connected.value = true
  toast.success('Conectado al chat')
})

onUnmounted(() => {
  // TODO: Disconnect from WebSocket
  connected.value = false
})
</script>