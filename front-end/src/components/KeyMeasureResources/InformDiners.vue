<template>
  <router-link :to="{ name: 'GeneratePosterPage' }" class="resource poster">
    <div class="link-icon"><i class="fas fa-bullhorn"></i></div>
    <p>
      L’information convives, par mail et par affichage, de la part de bio,
      durable et commerce équitable est d’ores et déjà en vigueur. Pour générer votre affiche, tester notre formulaire.
    </p>
    <div class="link-icon"><i class="fas fa-arrow-circle-right"></i></div>
  </router-link>
</template>

<style scoped lang="scss">
  @import '@/styles/key-measure-resource.scss';

  .resource.poster {
    background: $light-pink;
    border-color: $pink;

    .fa-bullhorn {
      color: $light-grey;
    }

    .fa-arrow-circle-right {
      color: $pink;
    }

    p {
      color: $pink;
    }
  }
</style>