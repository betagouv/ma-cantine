<script setup>
import AppBadgeSiretSiren from "@/components/AppBadgeSiretSiren.vue"
import AppBadgeCanteen from "@/components/AppBadgeCanteen.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import documentation from "@/data/documentation.json"

defineProps(["canteen"])
</script>

<template>
  <div class="tunnel-teledeclaration-sidebar fr-background-alt--blue-france fr-pb-4w">
    <div class="fr-pt-4w fr-pr-4w ma-cantine--sticky__top">
      <div class="ma-cantine--z-index-1">
        <div class="fr-mb-4w">
          <h2 class="fr-h4 fr-mb-1w">{{ canteen?.name }}</h2>
          <div>
            <AppBadgeCanteen :canteen="canteen" class="fr-mr-1w" />
            <AppBadgeSiretSiren :canteen="canteen" />
          </div>
        </div>
        <AppSeparator class="fr-mb-2w" />
        <div>
          <h3 class="fr-text--sm ma-cantine--text-uppercase fr-mb-1w">Approvisionnements</h3>
          <nav class="tunnel-teledeclaration-sidebar__nav">
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-fill"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Informations"
            />
            <DsfrButton
              secondary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Couverts annuels"
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="EGalim (obligatoire)"
              disabled
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Origine France et UE"
              disabled
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="« Local » et circuit court"
              disabled
            />
          </nav>
        </div>
        <AppSeparator class="fr-my-2w" />
        <div>
          <h3 class="fr-text--sm ma-cantine--text-uppercase fr-mb-1w">
            Volets thématiques
          </h3>
          <nav class="tunnel-teledeclaration-sidebar__nav">
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Infos convives"
              disabled
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Gaspillage"
              disabled
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Menus végétariens"
              disabled
            />
            <DsfrButton
              tertiary
              icon="fr-icon-checkbox-circle-line"
              class="tunnel-teledeclaration-sidebar__link fr-background-default--grey"
              label="Subsitutions plastiques"
              disabled
            />
          </nav>
        </div>
        <AppSeparator class="fr-my-2w" />
        <DsfrButton
          secondary
          icon="fr-icon-flag-fill"
          label="Récapitulatif"
          disabled
          class="tunnel-teledeclaration-sidebar__link"
        />
        <div class="fr-mt-2w ma-cantine--sticky__bottom">
          <AppHelpCard title="Centre d’aide" content="Votre télédéclaration pas à pas" class="tunnel-teledeclaration-sidebar__help-card">
            <a :href="documentation.teledeclaration" target="_blank">Je consulte l’aide</a>
          </AppHelpCard>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-sidebar {
  position: relative;
  &:before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 100vw;
    height: 100%;
    background-color: inherit;
  }

  &__nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  &__link {
    width: 100%;
  }

  &__help-card {
    background-color: transparent !important;
  }
}
</style>
