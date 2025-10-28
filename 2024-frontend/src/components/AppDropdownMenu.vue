<script setup>
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
import { useWindowSize } from "@vueuse/core"
defineProps(["label", "icon"])

/* Icon */
const isOpened = ref(false)
const arrow = computed(() => {
  const direction = isOpened.value ? "up" : "down"
  return `fr-icon-arrow-${direction}-s-line`
})

/* Dropdow alignment */
const { width } = useWindowSize()
const dropdownRef = useTemplateRef("dropdown-ref")
const dropdownAlign = computed(() => {
  const maxLeftPosition = width.value - 400 // 400px = 25rem
  const boundingRect = dropdownRef.value.getBoundingClientRect()
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
  <div class="app-dropdown-menu" ref="dropdown-ref">
    <DsfrButton
      class="app-dropdown-menu__opener"
      :class="{ hover: isOpened }"
      tertiary
      :icon="arrow"
      icon-right
      @click="isOpened = !isOpened"
      ref="opener"
      size="small"
    >
      <span :class="`${icon} ma-cantine--icon-xs`"></span>
      {{ label }}
    </DsfrButton>
    <div
      v-if="isOpened"
      :class="`app-dropdown-menu__content app-dropdown-menu__content--${dropdownAlign} fr-background-default--grey`"
      ref="content"
    >
      <slot></slot>
    </div>
  </div>
</template>

<style lang="scss">
.app-dropdown-menu {
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
    width: max-content;

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
}
</style>
