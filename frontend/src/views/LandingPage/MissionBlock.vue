<template>
  <v-row class="text-left">
    <v-col cols="12" sm="6" md="5" class="d-flex align-center">
      <div>
        <p>Notre mission :</p>

        <p class="font-weight-bold text-h6 mt-2">
          Accompagner la transition alimentaire dans les assiettes et les filières agricoles
        </p>
      </div>
    </v-col>
    <v-col cols="12" sm="6" md="7" class="pl-md-8">
      <p>Notre service « ma cantine » a vocation à :</p>
      <p class="mt-3">
        <span class="icon i-newspaper mr-2"></span>
        <strong>Informer, documenter et outiller</strong>
        les acteurs sur les bonnes pratiques en restauration collective
      </p>
      <p class="mt-3">
        <span class="icon i-restaurant mr-2"></span>
        <strong>Acroître la transparence</strong>
        de ce que nous mangeons dans nos réfectoires, hôpitaux...
      </p>
      <p class="mt-3">
        <span class="icon i-team mr-2"></span>
        <strong>Créer une communauté</strong>
        d'intérêts et de partage d'expériences autour du mieux manger
      </p>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "MissionBlock",
}
</script>

<style scoped>
.icon,
.icon::before {
  --icon-size: var(--icon-medium);
  --font-size: var(--icon-medium-font);
}
.icon::before {
  background: #424242;
}
</style>
