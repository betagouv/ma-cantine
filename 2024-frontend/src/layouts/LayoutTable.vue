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

  th:nth-child(1) {
    width: 35% !important;
  }

  td:nth-child(1),
  td:nth-child(4) {
    white-space: pre-wrap !important;
  }

  .fr-table__container {
    overflow: initial !important;
  }

  .fr-table {
    min-width: 55rem;
    width: 100%;
  }

  .fr-select {
    max-width: 7rem !important;
  }
}
</style>
