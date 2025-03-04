<template>
  <article class="app-ressources fr-card fr-col-12 fr-col-md-5 fr-p-7v fr-text-title--blue-france">
    <h3 class="ma-cantine--bold fr-mb-1w fr-text--lg ma-cantine--inherit-text-color">
      <span class="fr-icon-question-fill" aria-hidden="true"></span>
      Ressources utiles
    </h3>
    <ul class="app-ressources__list ma-cantine--unstyled-list fr-mb-0">
      <slot></slot>
    </ul>
  </article>
</template>

<style lang="scss">
.app-ressources {
  &__list {
    li:last-child {
      padding-bottom: 0 !important;
    }
  }
}
</style>
