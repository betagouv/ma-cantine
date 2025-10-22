<template>
  <div v-if="show" class="fr-notice fr-notice--info">
    <div class="fr-container">
      <div class="fr-notice__body">
        <p class="mb-0">
          <span class="fr-notice__title"></span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InformationBanner",
  data() {
    return {
      show: window.NOTICE_BANNER_SHOW,
    }
  },
}
</script>

<style lang="scss">
/*
  Copy/paste from DSFR style lib
  Not the best solution but the quickest before all pages are migrated to vue3
*/

.fr-notice {
  padding-bottom: 1rem;
  padding-top: 1rem;
  position: relative;

  &--info {
    background-color: #e8edff;
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

    &::before {
      mask-image: url(http://localhost:8000/2024-frontend/node_modules/@gouvfr/dsfr/dist/icons/system/fr--info-fill.svg);
      content: "";
      --icon-size: 1.5rem;
      background-color: currentColor;
      display: inline-block;
      flex: 0 0 auto;
      height: var(--icon-size);
      margin-right: 0.5rem;
      -webkit-mask-size: 100% 100%;
      mask-size: 100% 100%;
      vertical-align: calc((0.75em - var(--icon-size)) * 0.5);
      width: var(--icon-size);
    }
  }
}
</style>
