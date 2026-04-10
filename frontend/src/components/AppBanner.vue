<script>
/* eslint-disable */
</script>
<template>
  <div class="app-banner text-left">
    <div v-if="show" class="fr-notice fr-notice--info">
      <div class="fr-container">
        <div class="fr-notice__body">
          <p class="mb-0">
            <v-icon class="fr-notice__icon mr-2 mb-1">mdi-information</v-icon>
            <span class="fr-notice__title">{{ bannerTitle }}</span>
            <span class="fr-notice__desc">
              Valable uniquement pour les établissements qui ont validé leur télédéclaration dans les temps. Depuis
              votre bilan, vous pouvez corriger vos informations si besoin
              <a :href="bannerLink" target="_blank">
                voir l’article d’aide pour en savoir plus
                <v-icon small class="fr-notice__icon ml-1">mdi-open-in-new</v-icon>
              </a>.
            </span>
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
      publicBannerTitle: "DROIT À L’ERREUR : du 16 au 29 avril 2026.",
      loggedBannerTitle: "",
      bannerLink:
        "https://ma-cantine.crisp.help/fr/article/ou-trouver-lid-de-ma-cantine-ou-de-mon-groupe-th6t5u/",
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

  a {
    color: inherit;
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
