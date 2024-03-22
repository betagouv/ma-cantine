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
      <p class="mb-0">
        {{ measure.deadline.display }}
      </p>
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
      <ul>
        <li v-for="tag in measure.tags" :key="tag" class="my-2">
          {{ tagsInfo[tag] }}
        </li>
      </ul>
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

<style scoped>
ul {
  padding-left: 0;
  list-style-type: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
li::before {
  content: "\200B";
}
</style>
