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
