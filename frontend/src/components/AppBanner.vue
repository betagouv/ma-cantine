<template>
  <div class="app-banner">
    <div v-if="show" class="fr-notice fr-notice--info">
      <div class="fr-container">
        <div class="fr-notice__body">
          <p class="mb-0">
            <v-icon class="fr-notice__icon mr-2 mb-1">mdi-information</v-icon>
            <span class="fr-notice__title">{{ bannerTitle }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppBanner",
  data() {
    return {
      show: window.SHOW_BANNER,
      publicBannerTitle:
        "Campagne de télédéclaration du 12 au 31 mars 2026. Une prolongation de quelques jours est prévue - précisions le 31 mars.",
      loggedBannerTitle:
        "Campagne de télédéclaration 2026 : du 12 janvier au 31 mars 2026. Prolongation : télédéclarations possibles jusqu'à la campagne de correction - précisions le 31 mars.",
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
    bannerTitle() {
      return this.isAuthenticated && this.loggedBannerTitle ? this.loggedBannerTitle : this.publicBannerTitle
    },
  },
}
</script>

<style lang="scss">
/*
  Copy/paste from DSFR style lib
  Not the best solution but the quickest before all pages are migrated to vue3
*/

.app-banner .fr-notice {
  padding-bottom: 1rem;
  padding-top: 1rem;
  position: relative;

  &--info {
    background-color: #e8edff;
    color: #0063cb;
  }

  &__icon {
    color: #0063cb;
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

  &__title {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 700;
  }
}
</style>
