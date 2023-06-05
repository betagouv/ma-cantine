<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card outlined>
        <v-card-title class="text-body-1 font-weight-bold">
          <v-icon class="mr-2" size="20" color="red">mdi-food-apple</v-icon>
          Qualité des produits
        </v-card-title>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-row>
        <v-col cols="12">
          <v-card outlined>
            <v-card-title class="text-body-1 font-weight-bold">
              <v-icon class="mr-2" size="20" color="orange darken-2">mdi-offer</v-icon>
              Lutte contre le gaspillage
            </v-card-title>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card outlined>
            <v-card-title class="text-body-1 font-weight-bold">
              <v-icon class="mr-2" size="20" color="blue darken-1">mdi-weather-windy</v-icon>
              Interdiction du plastique
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="12" md="4">
      <v-row>
        <v-col cols="12">
          <v-card outlined>
            <v-card-title class="text-body-1 font-weight-bold">
              <v-icon class="mr-2" size="20" color="green darken-2">$leaf-fill</v-icon>
              Diversification des menus
            </v-card-title>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card outlined>
            <v-card-title class="text-body-1 font-weight-bold">
              <v-icon class="mr-2" size="20" color="amber darken-2">mdi-bullhorn</v-icon>
              Information des convives
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "EgalimProgression",
}
</script>
