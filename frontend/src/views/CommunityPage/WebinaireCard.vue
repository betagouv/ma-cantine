<template>
  <v-card class="pa-4 dsfr" :href="webinaire.link" outlined :ripple="false">
    <v-row>
      <v-col cols="1" v-if="$vuetify.breakpoint.smAndUp" class="justify-center align-center d-flex">
        <v-avatar color="secondary lighten-1" size="40">
          <v-icon>{{ icon }}</v-icon>
        </v-avatar>
      </v-col>
      <v-col cols="12" sm="3" class="align-center d-flex">
        <div class="font-weight-bold">{{ webinaire.title }}</div>
      </v-col>
      <v-col cols="12" sm="5" class="align-center d-flex body-2">
        {{ webinaire.tagline }}
      </v-col>
      <v-col cols="12" sm="3" class="align-center d-flex">
        <div class="d-flex flex-column">
          <div class="font-weight-bold body-1">{{ date }}</div>
          <div class="body-2 my-2">
            <v-icon small color="primary">mdi-map-marker</v-icon>
            {{ webinaire.address || "Visio - conférence" }}
          </div>
          <v-btn color="primary" width="120">
            Je m'inscris
            <span class="d-sr-only">à {{ webinaire.title }}</span>
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
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
      if (this.webinaire.type === "IN_PERSON") return "mdi-account-supervisor"
      return "mdi-television-play"
    },
    date() {
      return new Date(this.webinaire.startDate).toLocaleString("fr", {
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
