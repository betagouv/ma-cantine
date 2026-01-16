<template>
  <div class="layout-big-table">
    <div class="layout-big-table__scrollable">
      <slot />
    </div>
  </div>
</template>

<style lang="scss">
.layout-big-table {
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
    min-width: 75rem;
  }
}
</style>
