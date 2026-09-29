<script setup>
defineProps(["thematiques", "anchorName", "isTeledeclared", "appro"])
const emit = defineEmits(["openAccordion"])

/* Action */
const clickLink = (index) => emit("openAccordion", index)
</script>

<template>
  <div class="diagnostic-summary-tile">
    <div class="fr-tile" :class="{ 'fr-tile--blue': isTeledeclared }">
      <div class="fr-tile__title fr-grid-row">
        <div class="diagnostic-summary-tile__appro ma-cantine--flex-gap-1 fr-col-8">
          <img :src="appro.image" alt="" class="diagnostic-summary-tile__image" />
          <div>
            <a :href="`#${anchorName}`" @click="clickLink(0)" class="fr-text--regular fr-text-title--grey fr-text--md">
              {{ appro.title }}
            </a>
          </div>
        </div>
        <ul class="ma-cantine--unstyled-list fr-col-4">
          <li v-for="(volet, index) in thematiques" :key="volet.title" class="ma-cantine--flex-start ma-cantine--flex-gap-1 fr-mb-1w">
            <img :src="volet.image" alt="" class="diagnostic-summary-tile__image" />
            <a :href="`#${anchorName}`" @click="clickLink(index + 1)" class="fr-text--regular fr-text-title--grey fr-text--md">
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
  .fr-tile--blue .fr-tile__title::before {
    background-image: linear-gradient(0deg,var(--border-active-blue-france),var(--border-active-blue-france)) !important;
  }

  &__appro {
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 0.5rem;
    text-align: left;
  }

  &__image {
    width: 2rem;
    height: 2rem;
  }
}
</style>
