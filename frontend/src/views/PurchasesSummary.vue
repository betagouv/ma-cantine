<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PurchasesHome' } }]" />
    <div>
      <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
        La synthèse de mes achats
      </h1>
      <p>
        Choisissez la cantine et l'année pour voir la répartition par label de vos achats
      </p>
      <v-row class="mb-2">
        <v-col cols="12" sm="6">
          <DsfrAutocomplete
            hide-details="auto"
            :items="userCanteens"
            placeholder="Choisissez la cantine"
            v-model="vizCanteen"
            item-text="name"
            item-value="id"
            id="canteen"
            auto-select-first
            no-data-text="Pas de résultats"
            label="Cantine"
          />
        </v-col>
        <v-col cols="12" sm="4">
          <DsfrSelect label="Année" v-model="vizYear" :items="allowedYears" hide-details="auto" />
        </v-col>
      </v-row>
      <FamiliesGraph v-if="summary" :diagnostic="summary" :height="$vuetify.breakpoint.xs ? '440px' : '380px'" />
      <!-- TODO: a11y description -->
    </div>
  </div>
</template>

<script>
import { lastYear, diagnosticYears, normaliseText } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import FamiliesGraph from "@/components/FamiliesGraph"

export default {
  name: "PurchasesSummary",
  components: { BreadcrumbsNav, DsfrSelect, DsfrAutocomplete, FamiliesGraph },
  data() {
    return {
      vizYear: lastYear(),
      vizCanteen: null,
      allowedYears: diagnosticYears().map((year) => {
        return {
          text: year + (year > lastYear() ? " (prévisionnel)" : ""),
          value: year,
        }
      }),
      summary: null,
    }
  },
  computed: {
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
  },
  methods: {
    getCharacteristicByFamilyData() {
      if (!this.vizCanteen || !this.vizYear) return
      fetch(`/api/v1/canteenPurchasesSummary/${this.vizCanteen}?year=${this.vizYear}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          this.summary = response
        })
    },
  },
  watch: {
    vizCanteen(newCanteen) {
      if (newCanteen) this.getCharacteristicByFamilyData()
    },
    vizYear(newYear, oldYear) {
      if (oldYear && newYear) this.getCharacteristicByFamilyData()
    },
  },
  mounted() {
    if (this.userCanteens && this.userCanteens.length > 0) this.vizCanteen = this.userCanteens[0].id
  },
}
</script>
