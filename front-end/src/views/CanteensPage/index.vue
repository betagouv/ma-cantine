<template>
  <div>
    <div id="welcome-block">
      <h1>
        Découvrez les initiatives prises par nos cantines
        pour une alimentation plus durable
      </h1>
      <img src="@/assets/desktop.svg" alt="">
    </div>

    <div id="router-view">
      <router-view :key="$route.fullPath"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
  #welcome-block {
    display: flex;
    justify-content: center;
    padding: 3em;
    padding-bottom: 0;
    text-align: left;

    h1 {
      max-width: 730px;
    }

    img {
      height: 20em;
      padding-left: 3em;
    }
  }

  @media (max-width: 1000px) {
    #welcome-block {
      margin-bottom: 3em;
      text-align: center;

      img {
        display: none;
      }
    }
  }
</style>
