<template>
  <v-card outlined>
    <v-card-title>
      <h2 v-if="forMeasure" class="font-weight-bold text-body-1">
        <v-icon small class="mr-2" color="grey darken-4">$calendar-2-fill</v-icon>
        Entrée en vigueur
      </h2>
      <h3 v-else class="font-weight-bold text-body-1">
        <v-icon small class="mr-2" color="grey darken-4">$calendar-2-fill</v-icon>
        Entrée en vigueur
      </h3>
    </v-card-title>

    <v-card-text>
      {{ measure.deadline.display }}
    </v-card-text>

    <v-card-title>
      <h2 v-if="forMeasure" class="font-weight-bold text-body-1">
        <v-icon small class="mr-2" color="grey darken-4">$team-fill</v-icon>
        Pour qui ?
      </h2>
      <h3 v-else class="font-weight-bold text-body-1">
        <v-icon small class="mr-2" color="grey darken-4">$team-fill</v-icon>
        Pour qui ?
      </h3>
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
    forMeasure: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      tagsInfo: tags,
    }
  },
}
</script>
