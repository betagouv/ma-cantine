<script setup>
/*
  NOT A DSFR component yet : https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/menu-deroulant
  Needs to be updated when available in vue-dsfr package
*/
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
defineProps(["label", "icon", "links", "size"])
const emit = defineEmits(["click"])

/* Icon */
const isOpened = ref(false)
const arrow = computed(() => {
  const direction = isOpened.value ? "up" : "down"
  return `fr-icon-arrow-${direction}-s-line`
})

/* Click emit */
const clickEmitLink = (emitEvent) => {
  isOpened.value = false
  emit("click", emitEvent)
}

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
      tertiary
      :class="{ 'fr-background-contrast--blue-france': isOpened }"
      :icon="arrow"
      icon-right
      @click="isOpened = !isOpened"
      ref="opener"
      :size="size"
    >
      <span :class="`${icon} ma-cantine--icon-xs`"></span>
      {{ label }}
    </DsfrButton>
    <ul
      v-if="isOpened"
      class="app-dropdown-menu__content fr-background-default--grey ma-cantine--shadow-raised ma-cantine--unstyled-list fr-my-0"
      ref="content"
    >
      <li v-for="link, index in links" :key="index" class="fr-pb-0">
        <router-link
          v-if="link.to"
          :to="link.to"
          class="app-dropdown-menu__link ma-cantine--unstyled-link fr-text-title--blue-france fr-py-1v fr-px-3v fr-nav__link"
        >
          <p class="fr-text--sm ma-cantine--text-right fr-col-12 fr-mb-0">{{ link.label }}</p>
        </router-link>
        <a v-else
          href="#"
          class="app-dropdown-menu__link ma-cantine--unstyled-link fr-text-title--blue-france fr-py-1v fr-px-3v fr-nav__link fr-text--sm"
          @click.prevent="clickEmitLink(link.emitEvent)">
          <span class="ma-cantine--text-right fr-col-12">{{ link.label }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style lang="scss">
.app-dropdown-menu {
  position: relative;

  &__content {
    z-index: 9;
    position: absolute;
    bottom: 0;
    right: 0;
    left: auto;
    transform: translateY(100%);
    width: max-content !important;
  }

  &__link {
    min-height: 1rem !important;
    font-weight: initial !important;
    border-bottom: solid 1px var(--background-contrast-grey);
  }
}
</style>
