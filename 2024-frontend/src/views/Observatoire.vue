<script setup>
import { useTemplateRef } from "vue"
import ObservatoryHero from "@/components/ObservatoryHero.vue"
import ObservatoryFilters from "@/components/ObservatoryFilters.vue"
import ObservatoryResultsFilters from "@/components/ObservatoryResultsFilters.vue"

const filtersRef = useTemplateRef("filters-ref")

const scrollToFilters = () => {
  filtersRef.value.scrollIntoView({ behavior: "smooth" })
}
</script>

<template>
  <ObservatoryHero />
  <section class="fr-pt-5w" ref="filters-ref">
    <h2 class="fr-h5">Retrouver les chiffres clés sur votre territoire</h2>
    <ObservatoryFilters />
  </section>
  <section class="observatoire__results ma-cantine--sticky__container fr-mt-4w fr-pb-4w">
    <ObservatoryResultsFilters @scrollToFilters="scrollToFilters()" class="ma-cantine--sticky__top" />
    <DsfrNotice
      class="fr-my-2w"
      title="Pour des raisons de confidentialité, les cantines des armées ne sont pas intégrées dans cet observatoire."
    />
    <div style="height: 100vh"></div>
  </section>
</template>

<style lang="scss">
.observatoire {
  &__force-title-download-vertical {
    align-items: center !important;
    flex-direction: column !important;
    justify-content: center !important;
    text-align: center !important;

    .fr-tile__content {
      align-items: center !important;
    }

    .fr-tile__header {
      margin-right: 0 !important;
      margin-bottom: 1rem !important;
    }

    .fr-tile__pictogram {
      height: 3.5rem !important;
    }
  }

  &__results {
    &::before {
      z-index: -1;
      content: "";
      background-color: var(--background-alt-blue-france);
      position: absolute;
      top: 0;
      left: calc((100vw - 100%) / 2 * -1);
      width: 100vw;
      height: 100%;
    }
  }
}
</style>
