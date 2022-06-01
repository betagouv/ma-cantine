<template>
  <v-card class="pa-4">
    <v-row>
      <v-col cols="1" v-if="$vuetify.breakpoint.smAndUp" class="justify-center align-center d-flex">
        <v-avatar color="secondary lighten-1" size="40">
          <v-icon :aria-label="ariaLabel" aria-hidden="false">{{ icon }}</v-icon>
        </v-avatar>
      </v-col>
      <v-col cols="12" sm="4" class="align-center d-flex">
        <div class="font-weight-bold">{{ webinaire.title }}</div>
      </v-col>
      <v-col cols="12" sm="4" class="align-center d-flex body-2">
        {{ webinaire.description }}
      </v-col>
      <v-col cols="12" sm="3" class="align-center d-flex">
        <div class="d-flex flex-column">
          <div class="font-weight-bold body-1">{{ date }}</div>
          <div class="body-2 my-2">
            <v-icon small color="primary">mdi-map-marker</v-icon>
            {{ webinaire.address || "Visio - conférence" }}
          </div>
          <v-btn outlined color="primary" width="120">Je m'inscris</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { formatDate } from "@/utils"

export default {
  name: "WebinaireCard",
  props: {
    webinaire: {
      type: Object,
      required: true,
    },
  },
  computed: {
    icon() {
      if (this.webinaire.type === "VISIO") return "mdi-television-play"
      return "mdi-account-supervisor"
    },
    ariaLabel() {
      if (this.webinaire.type === "VISIO") return "Webinaire en visio-conférence"
      return "Webinaire présentiel"
    },
    date() {
      return formatDate(this.webinaire.date, {
        month: "long",
        day: "numeric",
        timeZone: "Europe/Paris",
        hour: "numeric",
        minute: "numeric",
        hour12: false,
      })
    },
  },
}
</script>
