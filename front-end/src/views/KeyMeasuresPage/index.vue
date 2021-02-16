<template>
  <nav id="measures-nav">
    <router-link :to="{ name: 'KeyMeasuresHome' }" class="nav-item">Tableau de bord</router-link>
    <template v-for="measure in keyMeasures" :key="measure.id">
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" class="nav-item">
        {{ measure.id }}
      </router-link>
    </template>
  </nav>

  <div id="router-view">
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<script>
  import keyMeasures from '@/data/key-measures.json'

  export default {
    data() {
      return {
        keyMeasures,
      };
    }
  }
</script>

<style scoped lang="scss">
  #router-view {
    padding: 1em 0.5em;
    max-width: 1170px;
    margin: auto;
  }

  #measures-nav {
    display: flex;
    justify-content: space-around;
    max-width: 1170px;
    margin: 8em auto 0 auto;
  }

  a {
    text-decoration: none;
  }

  .nav-item {
    color: $grey;
    padding: 10px;
    border-radius: 20px;
    margin: 0 3px;
  }

  .nav-item:hover, .router-link-exact-active {
    background-color: $light-orange;
  }

  @media (max-width: 750px) {
    #measures-nav {
      flex-direction: column;
      margin-top: 6em;
    }

    .nav-item {
      margin: 3px 0;
    }
  }

  @media (max-width: 480px) {
    #measures-nav {
      margin-top: 2em;
    }
  }
</style>
