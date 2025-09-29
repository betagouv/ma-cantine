<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr no-hover pa-sm-6">
    <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes satellites</h3></v-card-title>
    <v-card-text v-if="!satellites.length" class="fr-text-xs grey--text text--darken-2 mt-3 pb-0">
      <p class="mb-0">Ajoutez et publiez les cantines que vous livrez</p>
    </v-card-text>
    <v-spacer v-if="!satellites.length" />
    <v-card-text
      :class="`fr-text-xs mt-3 pb-0 ${hasSatelliteInconsistency ? 'dark-orange' : 'grey--text text--darken-2'}`"
      v-if="canteen.satelliteCanteensCount"
    >
      <p class="mb-0 d-flex">
        <v-icon small v-if="hasSatelliteInconsistency" class="mr-1 dark-orange">$alert-line</v-icon>
        {{ satelliteCountEmpty }}
      </p>
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
        <!-- TODO: does it still make sense to include the publication status? Maybe TD status is better -->
        <template v-slot:[`item.publicationStatus`]="{ item }">
          <PublicationBadge :isPublished="isSatellitePublished(item)" />
        </template>
      </v-data-table>
    </v-card-text>
    <v-spacer />
    <v-card-actions class="flex-wrap">
      <p class="mx-2 mb-2">
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
      </p>
    </v-card-actions>
  </v-card>
</template>

<script>
import PublicationBadge from "@/components/PublicationBadge"
import { hasSatelliteInconsistency } from "@/utils"

export default {
  name: "SatellitesWidget",
  components: { PublicationBadge },
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
  computed: {
    hasSatelliteInconsistency() {
      return hasSatelliteInconsistency(this.canteen)
    },
    satelliteCountEmpty() {
      const satPluralize = this.canteen.satelliteCanteensCount > 1 ? "satellites" : "satellite"
      const fillPluralize = this.canteen.satellites.length > 1 ? "renseignés" : "renseigné"
      return `${this.canteen.satellites.length} sur ${this.canteen.satelliteCanteensCount} ${satPluralize} ${fillPluralize}`
    },
  },
  methods: {
    updateSatelliteCount() {
      if (!this.canteen.isCentralCuisine) return
      const url = `/api/v1/canteens/${this.canteen.id}/satellites?limit=3`
      fetch(url)
        .then((response) => response.json())
        .then((response) => {
          this.satelliteCount = response.length
          this.satellites = response.split(0, 3)
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
