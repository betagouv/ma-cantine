<script setup>
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
import { useWindowSize } from "@vueuse/core"
defineProps(["label"])

/* Icon */
const isOpened = ref(false)
const icon = computed(() => {
  const direction = isOpened.value ? "up" : "down"
  return `fr-icon-arrow-${direction}-s-line`
})

/* Dropdow alignment */
const { width } = useWindowSize()
const filterRef = useTemplateRef("filter-ref")
const dropdownAlign = computed(() => {
  const maxLeftPosition = width.value - 400 // 400px = 25rem
  const boundingRect = filterRef.value.getBoundingClientRect()
  return boundingRect.left < maxLeftPosition ? "left" : "right"
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
  <div class="filter-by-base" ref="filter-ref">
    <DsfrButton
      class="filter-by-base__opener"
      :class="{ hover: isOpened }"
      tertiary
      :label="label"
      :icon="icon"
      icon-right
      @click="isOpened = !isOpened"
      ref="opener"
    />
    <div v-if="isOpened" :class="`filter-by-base__content filter-by-base__content--${dropdownAlign}`" ref="content">
      <div class="filter-by-base__scrollable fr-p-2w fr-mt-1v fr-card">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.filter-by-base {
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
    left: 0;
    transform: translateY(100%);

    @media (min-width: 768px) {
      &--right {
        right: 0;
        left: auto;
      }
      &--left {
        left: 0;
        right: auto;
      }
    }

    *:last-child {
      margin-bottom: 0 !important;
    }
  }

  &__scrollable {
    overflow-y: scroll;
    width: calc(100vw - 2rem);
    max-height: 25rem;

    @media (min-width: 768px) {
      width: 25rem;
    }
  }
}
</style>
