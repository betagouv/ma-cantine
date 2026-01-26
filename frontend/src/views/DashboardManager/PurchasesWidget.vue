<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr no-hover pa-sm-6">
    <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes achats</h3></v-card-title>
    <v-card-text class="fr-text-xs grey--text text--darken-2 py-0 mt-3">
      <p v-if="purchases.length">Source des données : {{ purchaseDataSourceString }}.</p>
      <p v-else>
        Renseignez vos achats pour calculer automatiquement votre progression sur le volet approvisionnements EGalim.
      </p>
    </v-card-text>
    <v-card-text class="pt-0">
      <v-data-table
        :items="purchases"
        :headers="purchaseHeaders"
        :hide-default-footer="true"
        :disable-sort="true"
        :class="`dsfr-table ${purchases.length && 'table-preview'}`"
        dense
      >
        <template v-slot:[`item.characteristics`]="{ item }">
          {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
        </template>
        <template v-slot:[`no-data`]>
          <v-card outlined rounded class="my-4 py-4 no-purchases" v-if="!purchasesFetchingError">
            <v-card-text class="fr-text-xs primary--text">
              <p class="mb-0">
                Saisissez vos achats manuellement ou connectez votre logiciel de gestion habituel.
              </p>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn :to="{ name: 'PurchasesHome' }" color="primary" class="mx-2 mb-2 fr-text-sm font-weight-medium">
                Compléter mes achats
              </v-btn>
            </v-card-actions>
          </v-card>
          <v-alert outlined type="error" v-else>
            <p>{{ purchasesFetchingError }}</p>
            <v-btn @click="fetchPurchases" outlined color="primary">Essayer à nouveau</v-btn>
          </v-alert>
        </template>
      </v-data-table>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions v-if="purchases.length || purchasesFetchingError" class="flex-wrap">
      <v-btn :to="{ name: 'NewPurchase' }" outlined color="primary" class="mx-2 mb-2">
        <v-icon small class="mr-2">$add-line</v-icon>
        Ajouter un achat
      </v-btn>
      <v-btn :to="{ name: 'GestionnaireImport' }" outlined color="primary" class="mx-2 mb-2 fr-btn--tertiary">
        <v-icon small class="mr-2">$file-add-line</v-icon>
        Importer des achats
      </v-btn>
      <v-btn :to="{ name: 'PurchasesHome' }" text color="primary" class="mx-2 mb-2">
        Voir tous mes achats
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { toCurrency } from "@/utils"
import Constants from "@/constants"

export default {
  name: "PurchasesWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      purchases: [],
      purchaseHeaders: [
        { text: "Date", value: "relativeDate" },
        { text: "Produit", value: "description" },
        { text: "Caractéristiques", value: "characteristics" },
        { text: "Prix HT", value: "priceHt" },
      ],
      purchasesFetchingError: null,
    }
  },
  computed: {
    canteenId() {
      return this.canteen.id
    },
    purchaseDataSourceString() {
      if (!this.purchases.length) return
      return this.purchases[0].creationSource === "APP" ? "ajout manuel" : "import en masse"
    },
  },
  methods: {
    fetchPurchases() {
      this.purchasesFetchingError = null
      const purchaseLimit = 3
      const query = `limit=${purchaseLimit}&ordering=-date&canteen__id=${this.canteenId}`
      return fetch(`/api/v1/purchases/?${query}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.purchases = response.results
          this.purchases.forEach((purchase) => {
            purchase.priceHt = toCurrency(purchase.priceHt)
            const dateDelta = Date.now() - new Date(purchase.date).getTime()
            const millisecondsInDay = 1000 * 60 * 60 * 24
            const daysAgo = Math.floor(dateDelta / millisecondsInDay)
            const weeksAgo = Math.floor(daysAgo / 7)
            const monthsAgo = Math.floor(daysAgo / 30)
            const yearsAgo = Math.floor(daysAgo / 365)
            if (yearsAgo > 0) {
              purchase.relativeDate = `il y a ${yearsAgo} an${yearsAgo === 1 ? "" : "s"}`
            } else if (monthsAgo > 0) {
              purchase.relativeDate = `il y a ${monthsAgo} mois`
            } else if (weeksAgo > 0) {
              purchase.relativeDate = `il y a ${weeksAgo} semaine${weeksAgo === 1 ? "" : "s"}`
            } else {
              purchase.relativeDate = `il y a ${daysAgo} jour${daysAgo === 1 ? "" : "s"}`
            }
          })
        })
        .catch(() => {
          this.purchases = []
          this.purchasesFetchingError = "Échec lors du téléchargement des achats"
        })
    },
    getProductCharacteristicsDisplayValue(characteristics) {
      const priorityOrder = Object.keys(Constants.Characteristics)
      characteristics = characteristics.filter((c) => priorityOrder.indexOf(c) > -1)
      characteristics.sort((a, b) => {
        return priorityOrder.indexOf(a) - priorityOrder.indexOf(b)
      })
      const displayCount = 3
      const remaining = characteristics.length - displayCount
      characteristics.splice(displayCount)
      let str = characteristics.map((c) => this.getCharacteristicDisplayValue(c).text).join(", ")
      if (remaining > 0) str += ` et ${remaining} autre${remaining > 1 ? "s" : ""}`
      return str
    },
    getCharacteristicDisplayValue(characteristic) {
      if (Object.prototype.hasOwnProperty.call(Constants.Characteristics, characteristic))
        return Constants.Characteristics[characteristic]
      return { text: "" }
    },
  },
  mounted() {
    this.fetchPurchases()
  },
  watch: {
    canteen(newCanteen, oldCanteen) {
      if (newCanteen && newCanteen.id !== oldCanteen?.id) {
        this.fetchPurchases()
      }
    },
  },
}
</script>

<style scoped>
.no-purchases {
  background-color: #f5f5fe;
  border: thin dashed #000091;
}
.v-application .rounded {
  border-radius: 8px !important;
}
</style>
