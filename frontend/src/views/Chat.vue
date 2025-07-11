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
            <span v-if="channel.unread_count > 0" class="badge badge-primary badge-sm ml-auto">
              {{ channel.unread_count }}
            </span>
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

        <div v-else-if="loadingMessages" class="flex justify-center items-center h-full">
          <span class="loading loading-spinner loading-lg"></span>
        </div>

        <div v-else v-for="message in messages" :key="message.id" class="chat" :class="message.user.id === currentUser?.id ? 'chat-end' : 'chat-start'">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img :src="message.user.avatar || `https://ui-avatars.com/api/?name=${message.user.first_name}+${message.user.last_name}`" />
            </div>
          </div>
          <div class="chat-header">
            {{ message.user.first_name }} {{ message.user.last_name }}
            <time class="text-xs opacity-50 ml-2">{{ formatTime(message.created_at) }}</time>
          </div>
          <div v-if="!message.is_deleted" class="chat-bubble" :class="message.user.id === currentUser?.id ? 'chat-bubble-primary' : ''">
            <div v-if="message.content" v-html="message.content" class="prose prose-sm max-w-none"></div>
            <div v-if="message.file" class="mt-2">
              <a v-if="message.file_type === 'document'" 
                :href="message.file_url" 
                target="_blank" 
                class="flex items-center gap-2 p-2 bg-base-200 rounded hover:bg-base-300"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {{ message.file_name }}
              </a>
              <img v-else 
                :src="message.file_url" 
                :alt="message.file_name"
                class="max-w-sm rounded cursor-pointer hover:opacity-90"
                @click="openImageModal(message.file_url)"
              />
            </div>
          </div>
          <div v-else class="chat-bubble opacity-50 italic">
            [Mensaje eliminado]
          </div>
          <div v-if="message.user.id === currentUser?.id && !message.is_deleted" class="chat-footer opacity-50 mt-1">
            <button @click="deleteMessage(message.id)" class="text-xs hover:text-error">
              Eliminar
            </button>
          </div>
        </div>

        <!-- Typing indicators -->
        <div v-for="(user, userId) in typingUsers" :key="`typing-${userId}`" class="chat chat-start">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img :src="`https://ui-avatars.com/api/?name=${user}`" />
            </div>
          </div>
          <div class="chat-bubble">
            <span class="loading loading-dots loading-sm"></span>
          </div>
        </div>
      </div>

      <!-- Message input -->
      <div v-if="selectedChannel" class="border-t p-4">
        <!-- File preview -->
        <div v-if="filePreview" class="mb-2 p-2 bg-base-200 rounded flex items-center justify-between">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
            <span class="text-sm">{{ filePreview.name }}</span>
          </div>
          <button @click="removeFile" class="btn btn-ghost btn-xs">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="sendMessage" class="flex gap-2">
          <div class="flex-1 relative">
            <textarea 
              v-model="newMessage"
              @input="handleTyping"
              @keydown.enter.prevent="handleEnterKey"
              placeholder="Escribe un mensaje... (Soporta Markdown)" 
              class="textarea textarea-bordered w-full resize-none"
              rows="1"
              :disabled="!connected"
            ></textarea>
            
            <!-- File upload button -->
            <label class="absolute right-2 top-2 cursor-pointer">
              <input 
                type="file" 
                @change="handleFileSelect"
                accept=".png,.jpg,.jpeg,.gif,.pdf,.docx,.xlsx,.doc,.xls"
                class="hidden"
              />
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 hover:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
            </label>
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="(!newMessage.trim() && !selectedFile) || !connected">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
        
        <div class="text-xs text-gray-500 mt-1">
          <span v-if="connected" class="text-success">● Conectado</span>
          <span v-else class="text-error">● Desconectado</span>
          <span class="ml-2">Soporta **negrita**, *cursiva*, `código` y más</span>
        </div>
      </div>
    </div>

    <!-- Online users sidebar -->
    <div class="w-64 bg-base-200 p-4 overflow-y-auto border-l">
      <h3 class="text-lg font-bold mb-4">Usuarios Online</h3>
      <ul class="space-y-2">
        <li v-for="user in onlineUsers" :key="user.id" class="flex items-center gap-2">
          <div class="avatar online">
            <div class="w-8 rounded-full">
              <img :src="user.avatar || `https://ui-avatars.com/api/?name=${user.name}`" />
            </div>
          </div>
          <span class="text-sm">{{ user.name }}</span>
        </li>
      </ul>
    </div>

    <!-- Image modal -->
    <dialog ref="imageModal" class="modal">
      <div class="modal-box max-w-4xl">
        <img :src="modalImageUrl" class="w-full" />
        <div class="modal-action">
          <button @click="closeImageModal" class="btn">Cerrar</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="closeImageModal">close</button>
      </form>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

const authStore = useAuthStore()
const toast = useToast()

// State
const currentUser = computed(() => authStore.currentUser)
const selectedChannel = ref(null)
const channels = ref([])
const messages = ref([])
const newMessage = ref('')
const connected = ref(false)
const loadingMessages = ref(false)
const messagesContainer = ref(null)
const onlineUsers = ref([])
const typingUsers = ref({})
const selectedFile = ref(null)
const filePreview = ref(null)
const imageModal = ref(null)
const modalImageUrl = ref('')

// WebSocket
let ws = null
let reconnectInterval = null
let typingTimeout = null

// Methods
const connectWebSocket = () => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const token = localStorage.getItem('access_token')
  const wsUrl = `${wsProtocol}//${window.location.host}/ws/chat/?token=${token}`
  
  ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    console.log('WebSocket connected')
    connected.value = true
    clearInterval(reconnectInterval)
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    handleWebSocketMessage(data)
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
    toast.error('Error de conexión')
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
    connected.value = false
    
    // Attempt to reconnect
    if (!reconnectInterval) {
      reconnectInterval = setInterval(() => {
        console.log('Attempting to reconnect...')
        connectWebSocket()
      }, 5000)
    }
  }
}

const handleWebSocketMessage = (data) => {
  switch (data.type) {
    case 'initial_data':
      channels.value = data.channels
      onlineUsers.value = data.online_users
      break
      
    case 'new_message':
      if (data.message.channel_id === selectedChannel.value?.id) {
        messages.value.push(data.message)
        scrollToBottom()
      } else {
        // Update unread count for other channels
        const channel = channels.value.find(c => c.id === data.message.channel_id)
        if (channel) {
          channel.unread_count = (channel.unread_count || 0) + 1
        }
      }
      break
      
    case 'user_online':
      if (!onlineUsers.value.find(u => u.id === data.user_id)) {
        onlineUsers.value.push({
          id: data.user_id,
          name: data.user_name,
          avatar: data.user_avatar
        })
      }
      break
      
    case 'user_offline':
      onlineUsers.value = onlineUsers.value.filter(u => u.id !== data.user_id)
      delete typingUsers.value[data.user_id]
      break
      
    case 'user_typing':
      if (data.channel_id === selectedChannel.value?.id) {
        if (data.is_typing) {
          typingUsers.value[data.user_id] = data.user_name
        } else {
          delete typingUsers.value[data.user_id]
        }
      }
      break
      
    case 'message_deleted':
      const messageIndex = messages.value.findIndex(m => m.id === data.message_id)
      if (messageIndex !== -1) {
        messages.value[messageIndex].is_deleted = true
        messages.value[messageIndex].content = '[Mensaje eliminado]'
      }
      break
      
    case 'error':
      toast.error(data.message)
      break
  }
}

const loadChannels = async () => {
  try {
    const response = await api.get('/chat/channels/')
    channels.value = response.data
  } catch (error) {
    console.error('Error loading channels:', error)
    toast.error('Error al cargar los canales')
  }
}

const selectChannel = async (channel) => {
  selectedChannel.value = channel
  channel.unread_count = 0
  loadingMessages.value = true
  
  try {
    // Load messages
    const response = await api.get(`/chat/channels/${channel.id}/messages/`)
    messages.value = response.data.results
    
    // Mark as read
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'mark_as_read',
        channel_id: channel.id
      }))
    }
    
    await api.post(`/chat/channels/${channel.id}/mark-read/`)
    
    scrollToBottom()
  } catch (error) {
    console.error('Error loading messages:', error)
    toast.error('Error al cargar los mensajes')
  } finally {
    loadingMessages.value = false
  }
}

const sendMessage = async () => {
  if ((!newMessage.value.trim() && !selectedFile.value) || !connected.value) return
  
  const messageData = {
    type: 'send_message',
    channel_id: selectedChannel.value.id,
    content: newMessage.value
  }
  
  // Handle file upload
  if (selectedFile.value) {
    const reader = new FileReader()
    reader.onload = (e) => {
      messageData.file = {
        name: selectedFile.value.name,
        content: e.target.result.split(',')[1] // Remove data:type;base64, prefix
      }
      
      // Send via WebSocket
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(messageData))
      }
      
      // Clear inputs
      newMessage.value = ''
      removeFile()
    }
    reader.readAsDataURL(selectedFile.value)
  } else {
    // Send text message
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(messageData))
    }
    newMessage.value = ''
  }
}

const handleTyping = () => {
  if (!selectedChannel.value || !connected.value) return
  
  // Clear existing timeout
  if (typingTimeout) {
    clearTimeout(typingTimeout)
  }
  
  // Send typing indicator
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'typing',
      channel_id: selectedChannel.value.id,
      is_typing: true
    }))
  }
  
  // Stop typing after 2 seconds
  typingTimeout = setTimeout(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'typing',
        channel_id: selectedChannel.value.id,
        is_typing: false
      }))
    }
  }, 2000)
}

const handleEnterKey = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file size (20MB)
  if (file.size > 20 * 1024 * 1024) {
    toast.error('El archivo no puede superar los 20MB')
    return
  }
  
  // Validate file type
  const allowedExtensions = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx', 'doc', 'xls']
  const ext = file.name.split('.').pop().toLowerCase()
  if (!allowedExtensions.includes(ext)) {
    toast.error('Tipo de archivo no permitido')
    return
  }
  
  selectedFile.value = file
  filePreview.value = {
    name: file.name,
    size: (file.size / 1024 / 1024).toFixed(2) + ' MB'
  }
}

const removeFile = () => {
  selectedFile.value = null
  filePreview.value = null
}

const deleteMessage = (messageId) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'delete_message',
      message_id: messageId
    }))
  }
}

const openImageModal = (imageUrl) => {
  modalImageUrl.value = imageUrl
  imageModal.value.showModal()
}

const closeImageModal = () => {
  imageModal.value.close()
  modalImageUrl.value = ''
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const isToday = date.toDateString() === now.toDateString()
  
  if (isToday) {
    return new Intl.DateTimeFormat('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  } else {
    return new Intl.DateTimeFormat('es-ES', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }
}

// Lifecycle
onMounted(() => {
  loadChannels()
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
  if (reconnectInterval) {
    clearInterval(reconnectInterval)
  }
  if (typingTimeout) {
    clearTimeout(typingTimeout)
  }
})
</script>

<style scoped>
.prose {
  max-width: none;
}

.prose :deep(p) {
  margin: 0.5em 0;
}

.prose :deep(code) {
  @apply bg-base-300 px-1 py-0.5 rounded text-sm;
}

.prose :deep(pre) {
  @apply bg-base-300 p-3 rounded overflow-x-auto;
}

.prose :deep(blockquote) {
  @apply border-l-4 border-l-blue-500 pl-4 italic;
}

.textarea {
  min-height: 2.5rem;
  max-height: 10rem;
}
</style>