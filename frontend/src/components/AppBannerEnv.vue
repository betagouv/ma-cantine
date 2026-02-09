<template>
  <div class="app-banner-env">
    <div v-if="show" class="fr-notice fr-notice--info">
      <div class="fr-container">
        <div class="fr-notice__body">
          <p class="mb-0">
            <v-icon class="fr-notice__icon mr-2 mb-1">mdi-information</v-icon>
            <span class="fr-notice__title">Vous êtes sur l'environnement {{ envText }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppBannerEnv",
  computed: {
    envText() {
      if (window.ENVIRONMENT === "staging") return "DEV"
      if (window.ENVIRONMENT === "demo") return "DÉMO"
      return window.ENVIRONMENT
    },
  },
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

  &__title {
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 700;
  }
}
</style>
