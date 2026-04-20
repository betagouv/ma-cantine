<script setup>
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
import { useWindowSize } from "@vueuse/core"
defineProps(["label", "number"])

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
      :icon="icon"
      icon-right
      secondary
      @click="isOpened = !isOpened"
      ref="opener"
    >
      {{ label }}
      <span class="filter-by-base__number fr-ml-1w fr-text--sm">10</span>
    </DsfrButton>
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

  &__number {
    display: inline-block;
    color: var(--text-inverted-blue-france);
    position: relative;
    z-index: 1;
    top: -1px;

    &:before {
      content: "";
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 1.75rem;
      height: 1.75rem;
      background-color: var(--background-action-high-blue-france);
      border-radius: 100%;
      z-index: -1;
    }
  }
}
</style>
