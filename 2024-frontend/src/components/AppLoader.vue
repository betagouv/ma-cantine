<template>
  <div class="app-loader fr-grid-row fr-grid-row--top">
    <div class="app-loader__icon mdi mdi-loading"></div>
    <p class="fr-ml-1w fr-mb-0">Chargement en cours...</p>
  </div>
</template>

<style lang="scss">
.app-loader {
  &__icon {
    animation: spin 1s infinite forwards;
    display: inline-block;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
