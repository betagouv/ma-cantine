<script setup>
/*
  NOT A DSFR component yet : https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/menu-deroulant
  Needs to be updated when available in vue-dsfr package
*/
import { computed, ref, useTemplateRef } from "vue"
import { onClickOutside, useEventListener } from "@vueuse/core"
defineProps(["label", "icon", "links", "size"])
const emit = defineEmits(["click"])

/* Elements */
const opener = useTemplateRef("opener")
const content = useTemplateRef("content")
const dropdownRef = useTemplateRef("dropdown-ref")

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

/* Visibility */
const closeDropdown = () => {
  isOpened.value = false
}
const toggleDropdown = () => {
  isOpened.value = !isOpened.value
  if (isOpened.value) updatePosition()
}
onClickOutside(content, closeDropdown, { ignore: [opener] })

/* Position */
const contentStyle = ref({})
const updatePosition = () => {
  const rect = dropdownRef.value.getBoundingClientRect()
  contentStyle.value = {
    top: `${rect.bottom}px`,
    right: `${window.innerWidth - rect.right}px`,
  }
}

useEventListener( window, "scroll",
  () => { if (isOpened.value) updatePosition() },
  { capture: true }
)
useEventListener(window, "resize", () => { isOpened.value = false })
</script>

<template>
  <div class="app-dropdown-menu" ref="dropdown-ref">
    <DsfrButton
      tertiary
      :class="{ 'fr-background-contrast--blue-france': isOpened }"
      :icon="arrow"
      icon-right
      @click="toggleDropdown()"
      ref="opener"
      :size="size"
    >
      <span :class="`${icon} ma-cantine--icon-xs`"></span>
      {{ label }}
    </DsfrButton>
    <Teleport to="body">
      <ul
        v-if="isOpened"
        class="app-dropdown-menu__content fr-background-default--grey ma-cantine--shadow-raised ma-cantine--unstyled-list fr-my-0"
        ref="content"
        :style="contentStyle"
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
    </Teleport>
  </div>
</template>

<style lang="scss">
.app-dropdown-menu {
  position: relative;

  &__content {
    z-index: 9;
    position: fixed;
    width: max-content !important;
  }

  &__link {
    min-height: 1rem !important;
    font-weight: initial !important;
    border-bottom: solid 1px var(--background-contrast-grey);
  }
}
</style>
