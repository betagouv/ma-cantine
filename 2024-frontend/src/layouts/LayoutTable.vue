<template>
  <div class="layout-table">
    <div class="layout-table__scrollable">
      <slot />
    </div>
  </div>
</template>

<style lang="scss">
.layout-table {
  overflow-x: hidden;

  &__scrollable {
    overflow: scroll;
  }

  .fr-table__container {
    overflow: initial !important;
  }

  .fr-table {
    min-width: 55rem !important;
    width: 100% !important;
  }

  .fr-select {
    max-width: 7rem !important;
  }
}
</style>
