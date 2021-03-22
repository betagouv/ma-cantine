<template>
  <router-link :to="{ name: 'GeneratePosterPage' }" class="resource poster">
    <div class="resource-icon"><i class="fas fa-bullhorn"></i></div>
    <p class="resource-prompt">
      L’information convives, par mail et par affichage, de la part de bio,
      durable et commerce équitable est d’ores et déjà en vigueur. Pour générer votre affiche, tester notre formulaire.
    </p>
    <div class="resource-icon"><i class="fas fa-arrow-circle-right"></i></div>
  </router-link>
</template>

<style scoped lang="scss">
  .resource.poster {
    background: $light-pink;
    border-color: $pink;

    .fa-bullhorn {
      color: $light-grey;
    }

    .fa-arrow-circle-right {
      color: $pink;
    }

    .resource-prompt {
      color: $pink;
    }
  }
</style>