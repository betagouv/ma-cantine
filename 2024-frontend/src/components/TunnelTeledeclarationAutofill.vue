<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import { formatNumber } from "@/utils"
import IconOSA from "@/components/IconOSA.vue"

/* Stores */
const props = defineProps(["name", "value"])
const emit = defineEmits(["fill", "reset"])
const storePurchaseSummary = useStorePurchaseSummary()
const { purchaseSummary } = storeToRefs(storePurchaseSummary)

/* Content */
const amount = computed(() => purchaseSummary.value?.[props.name])
const label = computed(() => `${formatNumber(amount.value)}€ HT`)
const isSelected = computed(() => props.value !== null && props.value !== undefined && props.value !== "" && Number(props.value) === amount.value)

/* Actions */
const toggle = () => {
  if (isSelected.value) emit("reset")
  else emit("fill", amount.value)
}
</script>
<template>
  <div class="tunnel-teledeclaration-autofill fr-input">
    <DsfrTag small selectable :selected="isSelected" @select="toggle">
      <IconOSA class="tunnel-teledeclaration-autofill__logo fr-mr-1v" />
      {{ label }}
    </DsfrTag>
  </div>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-autofill {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
  width: auto;
  padding: 0 0.5rem;
  border-top-left-radius: 0;

  &__logo {
    height: 0.75rem;
  }
}
</style>
