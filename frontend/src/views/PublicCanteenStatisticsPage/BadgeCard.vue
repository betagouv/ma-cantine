<template>
  <v-card class="fill-height text-center pt-4 pb-2 px-2 d-flex flex-column" outlined>
    <v-img max-width="30" contain :src="`/static/images/badges/${measure.badgeId}.svg`" class="mx-auto" alt=""></v-img>
    <v-card-text class="mx-auto">
      <v-row class="align-end">
        <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ percentageAchieved }} %</span>
        <span class="text-body-2 grey--text text--darken-2">
          {{ measure.shortTitle.toLowerCase() }}
        </span>
      </v-row>
    </v-card-text>
    <v-card-actions class="px-1">
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" class="text-body-2">
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
