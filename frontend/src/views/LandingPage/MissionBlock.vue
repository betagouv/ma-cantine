<template>
  <v-row class="text-left">
    <v-col cols="12" sm="6" md="5" class="d-flex align-center">
      <h2>
        <span class="text-body-1">Notre mission :</span>
        <br />
        <span class="text-h3 mt-2">
          Accompagner la transition alimentaire dans les assiettes et les filières agricoles
        </span>
      </h2>
    </v-col>
    <v-col cols="12" sm="6" md="7" class="pl-md-8 text-body-1">
      <p>Notre service « ma cantine » a vocation à :</p>
      <p class="mt-3">
        <v-icon color="grey darken-3" class="mr-2">$newspaper-fill</v-icon>
        <strong>Informer, documenter et outiller</strong>
        les acteurs sur les bonnes pratiques en restauration collective
      </p>
      <p class="mt-3">
        <v-icon color="grey darken-3" class="mr-2">$restaurant-fill</v-icon>
        <strong>Accroître la transparence</strong>
        de ce que nous mangeons dans nos réfectoires, hôpitaux...
      </p>
      <p class="mt-3">
        <v-icon color="grey darken-3" class="mr-2">$team-fill</v-icon>
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
