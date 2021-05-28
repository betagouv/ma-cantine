<template>
  <div>
    <v-card outlined tile>
      <v-row class="pa-3 justify-center">
        <v-col cols="12" sm="4" md="auto">
          <v-btn exact :to="{ name: 'KeyMeasuresHome' }" text small>
            Toutes les mesures
          </v-btn>
        </v-col>
        <v-col class="px-0" cols="12" sm="4" md="auto" v-for="measure in keyMeasures" :key="measure.id">
          <v-btn exact :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" text small>
            {{ measure.shortTitle }}
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <div id="router-view">
      <router-view :key="$route.fullPath" />
    </div>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  data() {
    return {
      keyMeasures,
    }
  },
}
</script>

<style scoped lang="scss">
#router-view {
  padding: 1em 0.5em;
  max-width: 1170px;
  margin: auto;
}
</style>
