<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import { spaceTypeLabel } from '../spaceTypes'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const currentWall = computed(() => walls.value.find(w => w.id === wallId.value))
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
})
async function run(save) {
  out.value = save ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true }) : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}`)
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}（{{ spaceTypeLabel(w.space_type) }}）</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <div v-if="out">
    <span v-if="currentWall" class="badge" :class="{ 'badge-wet': currentWall.space_type==='wet' }">{{ spaceTypeLabel(currentWall.space_type) }}</span>
    <p><strong>订货 {{ out.order_rolls ?? out.rolls }} 卷</strong> · 基础 {{ out.rolls }} 卷 · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m</p>
    <p v-if="out.wet_extra_applied" class="badge badge-wet">潮湿加卷 +{{ out.order_rolls - out.rolls }} 卷</p>
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>
