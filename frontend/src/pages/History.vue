<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import { spaceTypeLabel } from '../spaceTypes'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page"><h1>记录</h1><ul>
    <li v-for="r in items" :key="r.id">
      {{ r.wall_name }}
      <span class="badge" :class="{ 'badge-wet': r.result?.space_type==='wet' }">[{{ spaceTypeLabel(r.result?.space_type) }}]</span>
      → 订货 {{ r.result?.order_rolls ?? r.result?.rolls }} 卷
      <span v-if="r.result?.base_rolls != null">（基础 {{ r.result.base_rolls }} 卷）</span>
    </li>
  </ul></div>
</template>
