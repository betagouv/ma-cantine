<template>
  <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
    <v-img max-width="30" contain :src="`/static/images/badges/${measure.badgeId}.svg`" class="mx-auto" alt=""></v-img>
    <v-card-title class="mx-auto">
      <v-row class="align-end">
        <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ percentageAchieved }} %</span>
        <span class="text-body-2 grey--text text--darken-2">
          {{ measure.shortTitle.toLowerCase() }}
        </span>
      </v-row>
    </v-card-title>
    <v-card-actions class="mx-auto">
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }">
        La mesure
      </router-link>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: ["measure", "percentageAchieved"],
}
</script>
