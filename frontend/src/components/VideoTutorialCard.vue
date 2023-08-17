<template>
  <v-card
    class="dsfr"
    outlined
    :to="{
      name: 'VideoTutorial',
      params: { webinaireUrlComponent: `${videoTutorial.id}--${videoTutorial.title}` },
    }"
  >
    <v-card-title class="text-body-1 font-weight-bold d-block">
      <v-icon color="grey darken-3" class="mr-1 mt-n1">$film-fill</v-icon>
      {{ videoTutorial.title }}
    </v-card-title>
    <v-card-text v-if="videoTutorial.description">{{ videoTutorial.description }}</v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 pt-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "VideoTutorialCard",
  props: {
    videoTutorial: {
      type: Object,
      required: true,
    },
  },
}
</script>
