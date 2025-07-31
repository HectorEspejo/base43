<template>
  <div class="overflow-x-auto">
    <table class="table" :class="tableClass">
      <!-- Head -->
      <thead v-if="!hideHeader">
        <tr>
          <th v-if="selectable" class="w-12">
            <label>
              <input
                type="checkbox"
                class="checkbox"
                :checked="isAllSelected"
                :indeterminate="isIndeterminate"
                @change="toggleSelectAll"
              />
            </label>
          </th>
          <th
            v-for="column in columns"
            :key="column.key"
            :class="column.headerClass"
            @click="column.sortable ? handleSort(column.key) : null"
            :style="{ cursor: column.sortable ? 'pointer' : 'default' }"
          >
            <div class="flex items-center gap-1">
              {{ column.label }}
              <span v-if="column.sortable && sortBy === column.key" class="text-xs">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
          </th>
          <th v-if="$slots.actions" class="text-right">Actions</th>
        </tr>
      </thead>
      
      <!-- Body -->
      <tbody>
        <tr v-if="loading" class="hover">
          <td :colspan="totalColumns" class="text-center py-8">
            <span class="loading loading-spinner loading-md"></span>
          </td>
        </tr>
        
        <tr v-else-if="!data.length" class="hover">
          <td :colspan="totalColumns" class="text-center py-8 text-gray-500">
            {{ emptyMessage }}
          </td>
        </tr>
        
        <tr
          v-else
          v-for="(row, index) in sortedData"
          :key="row[rowKey] || index"
          class="hover"
          :class="{ 'active': isSelected(row) }"
        >
          <td v-if="selectable">
            <label>
              <input
                type="checkbox"
                class="checkbox"
                :checked="isSelected(row)"
                @change="toggleSelect(row)"
              />
            </label>
          </td>
          <td
            v-for="column in columns"
            :key="column.key"
            :class="column.cellClass"
          >
            <slot :name="`cell-${column.key}`" :row="row" :value="getCellValue(row, column.key)">
              {{ formatCellValue(row, column) }}
            </slot>
          </td>
          <td v-if="$slots.actions" class="text-right">
            <slot name="actions" :row="row" :index="index" />
          </td>
        </tr>
      </tbody>
      
      <!-- Footer -->
      <tfoot v-if="$slots.footer">
        <tr>
          <slot name="footer" />
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  loading: Boolean,
  emptyMessage: {
    type: String,
    default: 'No data available'
  },
  selectable: Boolean,
  selected: {
    type: Array,
    default: () => []
  },
  hideHeader: Boolean,
  tableClass: String,
  sortable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:selected', 'sort'])

const sortBy = ref(null)
const sortOrder = ref('asc')

const totalColumns = computed(() => {
  let count = props.columns.length
  if (props.selectable) count++
  if (props.$slots.actions) count++
  return count
})

const sortedData = computed(() => {
  if (!props.sortable || !sortBy.value) {
    return props.data
  }
  
  return [...props.data].sort((a, b) => {
    const aVal = getCellValue(a, sortBy.value)
    const bVal = getCellValue(b, sortBy.value)
    
    if (aVal === bVal) return 0
    
    if (sortOrder.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
})

const isAllSelected = computed(() => {
  return props.data.length > 0 && props.selected.length === props.data.length
})

const isIndeterminate = computed(() => {
  return props.selected.length > 0 && props.selected.length < props.data.length
})

const getCellValue = (row, key) => {
  return key.split('.').reduce((obj, k) => obj?.[k], row)
}

const formatCellValue = (row, column) => {
  const value = getCellValue(row, column.key)
  
  if (column.formatter) {
    return column.formatter(value, row)
  }
  
  if (value === null || value === undefined) {
    return ''
  }
  
  return value
}

const isSelected = (row) => {
  return props.selected.some(item => item[props.rowKey] === row[props.rowKey])
}

const toggleSelect = (row) => {
  const newSelected = [...props.selected]
  const index = newSelected.findIndex(item => item[props.rowKey] === row[props.rowKey])
  
  if (index > -1) {
    newSelected.splice(index, 1)
  } else {
    newSelected.push(row)
  }
  
  emit('update:selected', newSelected)
}

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    emit('update:selected', [])
  } else {
    emit('update:selected', [...props.data])
  }
}

const handleSort = (key) => {
  if (!props.sortable) return
  
  if (sortBy.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = key
    sortOrder.value = 'asc'
  }
  
  emit('sort', { sortBy: sortBy.value, sortOrder: sortOrder.value })
}
</script>