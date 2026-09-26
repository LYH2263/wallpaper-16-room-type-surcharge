<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import { spaceTypeLabel } from '../spaceTypes'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/walls')).items })
</script>
<template>
  <div class="page"><h1>墙面列表</h1>
  <table>
    <tr><th>名称</th><th>周长</th><th>空间类型</th><th></th></tr>
    <tr v-for="w in items" :key="w.id">
      <td>{{ w.name }}</td>
      <td>{{ w.perimeter }}m</td>
      <td><span class="badge" :class="{ 'badge-wet': w.space_type==='wet' }">{{ spaceTypeLabel(w.space_type) }}</span></td>
      <td><router-link :to="`/walls/${w.id}`">详情</router-link></td>
    </tr>
  </table>
  </div>
</template>
