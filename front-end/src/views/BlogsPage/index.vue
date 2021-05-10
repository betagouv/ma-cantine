<template>
  <div id="blogs-page">
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<style scoped lang="scss">
  #blogs-page {
    max-width: 1170px;
    padding: 1em;
    margin: auto;
    margin-bottom: 5em;
  }
</style>
