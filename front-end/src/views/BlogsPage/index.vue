<template>
  <div id="blogs-page">
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<style scoped lang="scss">
  #blogs-page {
    max-width: 1170px;
    margin: auto;
    margin-top: 8em;
    margin-bottom: 5em;
  }
</style>
