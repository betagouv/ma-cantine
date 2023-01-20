<template>
  <v-card
    class="fill-height text-center pt-4 pb-2 px-2 d-flex flex-column"
    outlined
    style="max-height: 10rem; max-width: 20rem;"
  >
    <v-img max-width="30" contain :src="`/static/images/badges/${measure.badgeId}.svg`" class="mx-auto" alt=""></v-img>
    <v-card-text class="mx-auto px-1">
      <span class="grey--text text-h5 font-weight-black text--darken-2" style="line-height: inherit;">
        {{ percentageAchieved }} %
      </span>
      <span class="text-body-2 grey--text text--darken-2">
        {{ measure.shortTitle.toLowerCase() }}
      </span>
    </v-card-text>
    <v-card-actions class="px-1">
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" class="text-body-2">
        La mesure
        <span class="d-sr-only">{{ measure.shortTitle }}</span>
      </router-link>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: ["measure", "percentageAchieved"],
}
</script>
