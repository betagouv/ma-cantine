<script setup>
const props = defineProps(["name"])

const options = [
  {
    label: "Oui",
    id: `${props.name}-yes`,
    value: true,
  },
  {
    label: "Non",
    id: `${props.name}-no`,
    value: false,
  },
]
</script>

<template>
  <DsfrRadioButtonSet v-bind="$attrs" :options="options">
    <template v-slot:legend>
      {{ $attrs.legend }}
      <span v-if="$attrs.hint" class="fr-hint-text">{{ $attrs.hint }}</span>
    </template>
  </DsfrRadioButtonSet>
</template>
