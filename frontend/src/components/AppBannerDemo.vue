<template>
  <div class="app-banner-env text-left">
    <div v-if="show" class="fr-notice fr-notice--info">
      <div class="fr-container">
        <div class="fr-notice__body">
          <p class="mb-0">
            <v-icon class="fr-notice__icon mr-2 mb-1">mdi-information</v-icon>
            <span class="fr-notice__title">
              ATTENTION : Plateforme de test et de démonstration.
            </span>
            <span class="fr-notice__desc">
              Pour toute action officielle, rendez-vous sur la
              <a
                class="fr-notice__link"
                href="https://ma-cantine.agriculture.gouv.fr/"
                target="_blank"
                rel="noopener"
                title="plateforme ma cantine - nouvelle fenêtre"
              >
                plateforme ma cantine
                <v-icon small color="#b34000">mdi-open-in-new</v-icon></a
              >. Toutes les actions sont sans conséquence. Le comportement est figé sur la période de télédéclaration
              (possibilité de créer un bilan de l'année n-1 et de le télédéclarer / corriger jusqu'à la fin de l'année n)
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppBannerDemo",
  data() {
    return {
      show: window.ENVIRONMENT !== "prod",
    }
  },
}
</script>

<style lang="scss">
/*
  Copy/paste from DSFR style lib
  Not the best solution but the quickest before all pages are migrated to vue3
*/

.app-banner-env {
  position: sticky;
  top: 0;
  z-index: 3; // above the header (2) and the unfocused skip links (1)
}

.app-banner-env .fr-notice {
  padding-bottom: 1rem;
  padding-top: 1rem;
  position: relative;

  &--info {
    background-color: #ffe9e6;
    color: #b34000;
  }

  &__icon {
    color: #b34000;
  }

  .fr-container {
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 78rem;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
  }

  &__body {
    align-items: flex-start;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    position: relative;
  }

  &__link {
    color: inherit;
  }

  &__title {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 700;
  }
}
</style>
