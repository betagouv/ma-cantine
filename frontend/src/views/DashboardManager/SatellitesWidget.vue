<template>
  <v-card outlined class="fill-height d-flex flex-column pa-4">
    <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes satellites</h3></v-card-title>
    <v-card-text v-if="!satellites.length" class="fr-text-xs grey--text text--darken-2 mt-3 pb-0">
      <p class="mb-0">Ajoutez et publiez les cantines que vous livrez</p>
    </v-card-text>
    <v-spacer v-if="!satellites.length" />
    <v-card-text class="fr-text-xs grey--text text--darken-2 mt-3 pb-0" v-if="canteen.satelliteCanteensCount">
      <p class="mb-0">{{ satelliteCount }} / {{ canteen.satelliteCanteensCount }} satellites renseignés</p>
    </v-card-text>
    <v-spacer v-if="satellites.length" />
    <v-card-text class="py-0" v-if="satellites.length">
      <v-data-table
        :items="satellites"
        :headers="satelliteHeaders"
        :hide-default-footer="true"
        :disable-sort="true"
        :class="`dsfr-table grey--table ${satellites.length && 'table-preview'}`"
        dense
      >
        <template v-slot:[`item.publicationStatus`]="{ item }">
          <v-chip
            :color="isSatellitePublished(item) ? 'green lighten-4' : 'grey lighten-2'"
            :class="isSatellitePublished(item) ? 'green--text text--darken-4' : 'grey--text text--darken-2'"
            class="font-weight-bold px-2 fr-text-xs text-uppercase"
            style="border-radius: 4px !important;"
            small
            label
          >
            {{ isSatellitePublished(item) ? "Publiée" : "Non publiée" }}
          </v-chip>
        </template>
      </v-data-table>
    </v-card-text>
    <v-spacer />
    <v-card-actions class="ma-2">
      <v-btn
        :to="{
          name: 'SatelliteManagement',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
        }"
        color="primary"
        :outlined="!!satellites.length"
      >
        {{ satellites.length ? "Modifier" : "Ajouter mes satellites" }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "SatellitesWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      satellites: [],
      satelliteHeaders: [
        { text: "Nom", value: "name" },
        { text: "Statut", value: "publicationStatus" },
      ],
      satelliteCount: null,
    }
  },
  methods: {
    updateSatelliteCount() {
      if (!this.canteen.isCentralCuisine) return
      const url = `/api/v1/canteens/${this.canteen.id}/satellites?limit=3`
      fetch(url)
        .then((response) => response.json())
        .then((response) => {
          this.satelliteCount = response.count
          this.satellites = response.results
        })
    },
    isSatellitePublished(canteen) {
      return canteen.publicationStatus === "published"
    },
  },
  mounted() {
    this.updateSatelliteCount()
  },
  watch: {
    canteen(newCanteen, oldCanteen) {
      if (newCanteen && newCanteen.id !== oldCanteen?.id) {
        this.updateSatelliteCount()
      }
    },
  },
}
</script>
