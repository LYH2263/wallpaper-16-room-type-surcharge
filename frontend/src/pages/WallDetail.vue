<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
import { SPACE_TYPES, spaceTypeLabel } from '../spaceTypes'
const props = defineProps({ id: String })
const wall = ref(null)
const type = ref('normal')
const saving = ref(false)
const msg = ref('')
onMounted(async () => {
  wall.value = await getJSON(`/api/walls/${props.id}`)
  type.value = wall.value.space_type ?? 'normal'
})
async function save() {
  saving.value = true; msg.value = ''
  try {
    wall.value = await patchJSON(`/api/walls/${props.id}`, { space_type: type.value })
    msg.value = '已保存'
  } catch (e) {
    msg.value = `保存失败：${e.message}`
  } finally {
    saving.value = false
  }
}
</script>
<template>
  <div class="page" v-if="wall"><h1>{{ wall.name }}</h1>
  <p v-if="wall.data_quality==='dirty'" class="warn">{{ wall.note }}</p>
  <p>周长 {{ wall.perimeter }} m，墙高 {{ wall.height }} m</p>
  <div class="form-row">
    <span>空间类型：</span>
    <span class="badge" :class="{ 'badge-wet': type==='wet' }">{{ spaceTypeLabel(type) }}</span>
    <select v-model="type">
      <option v-for="t in SPACE_TYPES" :key="t.value" :value="t.value">{{ t.label }}</option>
    </select>
    <button :disabled="saving" @click="save">保存类型</button>
    <span v-if="msg" :class="{ 'saved-ok': msg==='已保存', 'warn': msg!=='已保存' }">{{ msg }}</span>
  </div></div>
</template>
