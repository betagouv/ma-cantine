<script setup>
defineProps(["thematiques", "anchorName", "isTeledeclared", "appro"])
import AppIconLink from "@/components/AppIconLink.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import IconAward from "@/components/IconAward.vue"

const emit = defineEmits(["openAccordion"])
const clickLink = (index) => emit("openAccordion", index)
</script>

<template>
  <div class="diagnostic-summary-tile">
    <div class="fr-tile">
      <div class="fr-tile__title fr-grid-row fr-text--regular fr-text-title--grey fr-text--md">
        <div class="diagnostic-summary-tile__appro-container ma-cantine--flex-gap-1 fr-col-8 fr-pr-8w">
          <img :src="appro.image" alt="" class="diagnostic-summary-tile__image" />
          <div class="ma-cantine--width-100">
            <a :href="`#${anchorName}`" @click="clickLink(0)" class="fr-text-default--grey">
              {{ appro.title }}
            </a>
            <div class="fr-grid-row fr-pt-1w">
              <AppIconLink class="fr-col-1" top="1.25rem" />
              <div class="fr-col-11">
                <ul class="ma-cantine--unstyled-list fr-pl-1w">
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square"></div>
                    <p class="fr-mb-0 fr-text--sm">Objectif EGalim</p>
                  </li>
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square"></div>
                    <p class="fr-mb-0 fr-text--sm">Objectif SIQO</p>
                  </li>
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square"></div>
                    <p class="fr-mb-0 fr-text--sm">Objectif Bio</p>
                  </li>
                </ul>
                <AppSeparator class="fr-my-3w" />
              </div>
            </div>
            <div class="fr-grid-row">
              <div class="fr-col-1">
                <IconAward class="diagnostic-summary-tile__award"/>
              </div>
              <div class="fr-col-11">
                <p class="fr-mb-0 fr-text--sm">Objectif viande et poisson</p>
              </div>
            </div>
          </div>
        </div>
        <ul class="diagnostic-summary-tile__thematiques-container ma-cantine--unstyled-list fr-my-0 fr-col-4">
          <li v-for="(volet, index) in thematiques" :key="volet.title" class="ma-cantine--flex-start ma-cantine--flex-gap-1">
            <img :src="volet.image" alt="" class="diagnostic-summary-tile__image" />
            <a :href="`#${anchorName}`" @click="clickLink(index + 1)" class="fr-text-default--grey">
              {{ volet.shortTitle }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.diagnostic-summary-tile {

  &__appro-container {
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 0.5rem;
    text-align: left;
  }

  &__thematiques-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 0.5rem;
  }

  &__image {
    width: 2rem;
    height: 2rem;
  }

  &__square {
    width: 0.5rem;
    height: 0.5rem;
    background-color: var(--border-default-grey);
  }

  &__award {
    color: var(--border-default-grey);
  }
}
</style>
