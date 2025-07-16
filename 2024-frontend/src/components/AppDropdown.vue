<script setup>
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
defineProps(["label"])

/* Icon */
const isOpened = ref(false)
const icon = computed(() => {
  const direction = isOpened.value ? "up" : "down"
  return `fr-icon-arrow-${direction}-s-line`
})

/* Click outside */
const opener = useTemplateRef("opener")
const content = useTemplateRef("content")
const closeDropdown = () => {
  isOpened.value = false
}
onClickOutside(content, closeDropdown, { ignore: [opener] })
</script>

<template>
  <div class="app-dropdow">
    <DsfrButton
      class="app-dropdow__opener"
      :class="{ hover: isOpened }"
      tertiary
      :label="label"
      :icon="icon"
      icon-right
      @click="isOpened = !isOpened"
      ref="opener"
    />
    <div v-if="isOpened" class="app-dropdow__content" ref="content">
      <div class="app-dropdow__scrollable fr-p-2w fr-mt-1v fr-card">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.app-dropdow {
  position: relative;

  &__opener {
    &.hover {
      background-color: var(--hover-tint);
    }
  }

  &__content {
    z-index: 9;
    position: absolute;
    bottom: 0;
    transform: translateY(100%);

    *:last-child {
      margin-bottom: 0 !important;
    }
  }

  &__scrollable {
    width: 25rem;
    max-height: 25rem;
    overflow-y: scroll;
  }
}
</style>
