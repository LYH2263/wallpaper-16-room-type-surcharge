export const SPACE_TYPES = [
  { value: 'normal', label: '普通' },
  { value: 'wet', label: '潮湿' },
]

export function spaceTypeLabel(v) {
  const hit = SPACE_TYPES.find(t => t.value === v)
  if (hit) return hit.label
  return v == null ? '—' : v
}
