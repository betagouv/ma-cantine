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

  th:nth-child(1) {
    width: 35% !important;
  }

  td:nth-child(1),
  td:nth-child(4) {
    white-space: pre-wrap !important;
  }
}

.layout-big-table__scrollable {
  overflow: scroll;
}

.layout-big-table .fr-table__container {
  overflow: initial !important;
}

.layout-big-table .fr-table {
  min-width: 75rem;
}

</style>
