<template>
  <v-row class="text-left">
    <v-col cols="12" sm="6" md="5" class="d-flex align-center">
      <div>
        <p class="mb-0">Notre mission :</p>

        <p class="font-weight-bold text-h6 mt-2">
          Accompagner la transition alimentaire dans les assiettes et les filières agricoles
        </p>
      </div>
    </v-col>
    <v-col cols="12" sm="6" md="7" class="pl-md-8">
      <p>Notre service « ma cantine » a vocation à :</p>
      <ul class="no-bullets">
        <li class="mt-3">
          <v-icon color="grey darken-3" class="mr-2">$newspaper-fill</v-icon>
          <strong>Informer, documenter et outiller</strong>
          les acteurs sur les bonnes pratiques en restauration collective
        </li>
        <li class="mt-3">
          <v-icon color="grey darken-3" class="mr-2">$restaurant-fill</v-icon>
          <strong>Accroître la transparence</strong>
          de ce que nous mangeons dans nos réfectoires, hôpitaux...
        </li>
        <li class="mt-3">
          <v-icon color="grey darken-3" class="mr-2">$team-fill</v-icon>
          <strong>Créer une communauté</strong>
          d'intérêts et de partage d'expériences autour du mieux manger
        </li>
      </ul>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "MissionBlock",
}
</script>
