<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const enabled = ref(true)
const extra = ref(1)
const saving = ref(false)
const msg = ref('')
onMounted(async () => {
  const s = await getJSON('/api/settings')
  enabled.value = s.wet_room_enabled ?? true
  extra.value = s.wet_room_extra_rolls ?? 1
})
async function save() {
  if (!Number.isInteger(extra.value) || extra.value < 0) {
    msg.value = '加卷枚数需为不小于 0 的整数'
    return
  }
  saving.value = true; msg.value = ''
  try {
    const s = await putJSON('/api/settings', { wet_room_enabled: enabled.value, wet_room_extra_rolls: extra.value })
    enabled.value = s.wet_room_enabled
    extra.value = s.wet_room_extra_rolls
    msg.value = '已保存'
  } catch (e) {
    msg.value = `保存失败：${e.message}`
  } finally {
    saving.value = false
  }
}
</script>
<template><div class="page"><h1>设置</h1>
  <div class="form-row">
    <label><input type="checkbox" v-model="enabled"> 启用潮湿空间加卷规则</label>
  </div>
  <div class="form-row">
    <label>潮湿加卷枚数 <input type="number" min="0" step="1" v-model.number="extra" :disabled="!enabled"></label>
  </div>
  <div class="form-row">
    <button :disabled="saving" @click="save">保存设置</button>
    <span v-if="msg" :class="{ 'saved-ok': msg==='已保存', 'warn': msg!=='已保存' }">{{ msg }}</span>
  </div>
  <p v-if="!enabled" class="warn">规则已停用：新测算订货卷数等于基础卷数（历史记录不受影响）。</p>
</div></template>
