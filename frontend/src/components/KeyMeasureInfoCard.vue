<template>
  <v-card outlined>
    <v-card-title class="font-weight-bold text-body-1">
      <v-icon small class="mr-2" color="grey darken-4">mdi-calendar-month</v-icon>
      Entrée en vigueur
    </v-card-title>

    <v-card-text>
      {{ measure.deadline.display }}
    </v-card-text>

    <v-card-title class="font-weight-bold text-body-1">
      <v-icon small class="mr-2" color="grey darken-4">mdi-chart-arc</v-icon>
      Pour qui ?
    </v-card-title>

    <v-card-text>
      <p v-if="measure.who">{{ measure.who }}</p>
      <div>
        <div v-for="tag in measure.tags" :key="tag" class="my-2">
          {{ tagsInfo[tag] }}
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import tags from "@/data/sector-tags.json"

export default {
  name: "KeyMeasureInfoCard",
  props: {
    measure: Object,
  },
  data() {
    return {
      tagsInfo: tags,
    }
  },
}
</script>
