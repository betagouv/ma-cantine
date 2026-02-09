<template>
  <div class="app-banner-alert">
    <div class="fr-notice fr-notice--alert">
      <div class="fr-container">
        <div class="fr-notice__body">
          <p class="mb-0">
            <v-icon class="fr-notice__icon mr-2 mb-1">mdi-information</v-icon>
            <span class="fr-notice__title">
              Gestionnaires de crèches : rappel de laits infantiles, voir les lots concernés sur le site
              <a href="https://rappel.conso.gouv.fr/categorie/25" target="_blank">
                Rappel conso
                <v-icon small class="ml-1">mdi-open-in-new</v-icon>
              </a>
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppBannerAlert",
  data() {
    return {
      show: window.SHOW_BANNER,
    }
  },
}
</script>

<style lang="scss">
/*
  Copy/paste from DSFR style lib
  Not the best solution but the quickest before all pages are migrated to vue3
*/

.app-banner-alert .fr-notice {
  padding-bottom: 1rem;
  padding-top: 1rem;
  position: relative;

  &--alert {
    background-color: #ffe9e9;
    color: #ce0500;
  }

  &__icon {
    color: #ce0500;
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

    a {
      color: inherit !important;
      text-decoration: underline !important;
    }
    i {
      color: inherit !important;
    }
  }
}
</style>
