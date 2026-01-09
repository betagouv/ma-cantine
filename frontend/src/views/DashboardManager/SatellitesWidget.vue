<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr no-hover pa-sm-6">
    <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes restaurants satellites</h3></v-card-title>
    <v-card-text v-if="!satellites.length" class="fr-text-xs grey--text text--darken-2 mt-3 pb-0">
      <p class="mb-0">Ajoutez les restaurants que vous livrez</p>
    </v-card-text>
    <v-spacer v-if="!satellites.length" />
    <v-card-text
      :class="`fr-text-xs mt-3 pb-0 ${hasSatelliteInconsistency ? 'dark-orange' : 'grey--text text--darken-2'}`"
    >
      <p class="mb-0 d-flex">
        <v-icon small v-if="hasSatelliteInconsistency" class="mr-1 dark-orange">$alert-line</v-icon>
        {{ satelliteCountSentence }}
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
        <template v-slot:[`item.action`]="{ item }">
          <DataInfoBadge
            :currentYear="isCurrentYear"
            :inTeledeclaration="inTeledeclarationCampaign"
            :inCorrection="inCorrectionCampaign"
            :canteenAction="item.action"
            class="my-2"
          />
        </template>
      </v-data-table>
    </v-card-text>
    <v-spacer />
    <v-card-actions class="flex-wrap">
      <p class="mx-2 mb-2">
        <v-btn
          :to="{
            name: 'GestionnaireCantineGroupeSatellites',
            params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
          }"
          color="primary"
          outlined
        >
          Gérer mes restaurants satellites
        </v-btn>
      </p>
    </v-card-actions>
  </v-card>
</template>

<script>
import DataInfoBadge from "@/components/DataInfoBadge"
import { hasSatelliteInconsistency, lastYear } from "@/utils"

export default {
  name: "SatellitesWidget",
  components: { DataInfoBadge },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      lastYear: lastYear(),
      satellites: [],
      satelliteHeaders: [
        { text: "Nom", value: "name" },
        { text: `Bilan ${lastYear()}`, value: "action" },
      ],
      isCurrentYear: false, // Table always display for previous year
      inTeledeclarationCampaign: false,
      inCorrectionCampaign: false,
    }
  },
  computed: {
    hasSatelliteInconsistency() {
      return hasSatelliteInconsistency(this.canteen)
    },
    satelliteCountSentence() {
      const count = this.canteen.satellitesCount
      if (count === 0) return "Aucun restaurant satellite renseigné"
      else if (count === 1) return "1 restaurant satellite renseigné"
      else return `${count} restaurants satellites renseignés`
    },
  },
  methods: {
    updateSatellites() {
      if (this.canteen.productionType !== "groupe") return
      const url = `/api/v1/canteens/${this.canteen.id}/satellites/`
      fetch(url)
        .then((response) => response.json())
        .then((response) => {
          let satellitesIncomplete = []
          let satellitesTeledeclared = []
          let satellitesOther = []
          for (const sat of response) {
            if (sat.action === "35_fill_canteen_data") satellitesIncomplete.push(sat)
            else if (sat.action === "95_nothing") satellitesTeledeclared.push(sat)
            else satellitesOther.push(sat)
          }
          const satellitesOrders = [...satellitesIncomplete, ...satellitesTeledeclared, ...satellitesOther]
          this.satellites = satellitesOrders.slice(0, 3)
        })
    },
    isSatellitePublished(canteen) {
      return canteen.publicationStatus === "published"
    },
    fetchCampaignDates() {
      fetch(`/api/v1/campaignDates/${this.lastYear}`)
        .then((response) => response.json())
        .then((response) => {
          this.inTeledeclarationCampaign = response.inTeledeclaration
          this.inCorrectionCampaign = response.inCorrection
        })
    },
  },
  mounted() {
    this.updateSatellites()
    this.fetchCampaignDates()
  },
  watch: {
    canteen(newCanteen, oldCanteen) {
      if (newCanteen && newCanteen.id !== oldCanteen?.id) {
        this.updateSatellites()
      }
    },
  },
}
</script>
