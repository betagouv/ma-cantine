<template>
  <div>
    <div v-if="noPurchases">
      <div class="overlay text-center py-8 px-16">
        <h4 class="fr-text font-weight-bold mb-4">Pilotez votre progression tout au long de l’année en cours</h4>
        <p class="fr-text">
          Avec l’outil de suivi d’achats de « ma cantine », pilotez en temps réel la part de vos approvisionnements qui
          correspondent aux critères de la loi EGAlim, et facilitez votre prochaine télédéclaration.
        </p>
        <p class="fr-text">
          Pour cela, vous pouvez renseigner tous vos achats au fil de l’eau ou par import en masse, ou bien connecter
          votre outil de gestion habituel si cela est possible pour transférer les données.
        </p>
        <v-btn large color="primary" :to="{ name: 'PurchasesHome' }">
          <span class="fr-text-lg">Commencer</span>
        </v-btn>
      </div>
    </div>
    <div v-else>
      <DsfrCallout icon="">
        <p class="fr-text font-weight-bold">Résultats intermédiaires</p>
        <p class="fr-text-sm grey-text text--darken-3">
          Les résultats ci-dessous sont calculés automatiquement à partir des données d’achats renseignées à date via
          l’outil de suivi d’achats de « ma cantine » pour l’année {{ year }}.
        </p>
        <v-row class="align-center my-4 mx-0">
          <v-btn class="mr-2" outlined color="primary" :to="{ name: 'PurchasesHome' }">Compléter mes achats</v-btn>
          <p v-if="lastPurchaseAddDate" class="fr-text-sm grey--text text--darken-3 mb-0">
            Dernières données :
            <b>{{ lastUpdate }}.</b>
          </p>
        </v-row>
      </DsfrCallout>
      <QualityMeasureSummary :canteen="canteen" :diagnostic="purchasesSummary" />
    </div>
  </div>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"
import QualityMeasureSummary from "./QualityMeasureSummary"
import { lastYear, timeAgo } from "@/utils"

export default {
  name: "PurchasesSummary",
  props: {
    diagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: {
    DsfrCallout,
    QualityMeasureSummary,
  },
  data() {
    return {
      year: lastYear() + 1,
      purchasesSummary: null,
      lastPurchaseAddDate: null,
    }
  },
  computed: {
    lastUpdate() {
      return this.lastPurchaseAddDate ? timeAgo(this.lastPurchaseAddDate, true) : null
    },
    noPurchases() {
      return !this.purchasesSummary?.valueTotalHt
    },
  },
  methods: {
    fetchPurchasesSummary() {
      if (this.canteen?.id) {
        return fetch(`/api/v1/canteenPurchasesSummary/${this.canteen.id}?year=${this.year}`)
          .then((response) => (response.ok ? response.json() : {}))
          .then((response) => (this.purchasesSummary = response))
      }
    },
    fetchLastAddedPurchase() {
      if (this.canteen?.id) {
        const query = `limit=1&ordering=-creation_date&canteen__id=${this.canteen.id}&date__year=${this.year}`
        return fetch(`/api/v1/purchases/?${query}`)
          .then((response) => {
            if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
            return response.json()
          })
          .then((response) => {
            const purchases = response.results
            this.lastPurchaseAddDate = purchases.length ? purchases[0].creationDate : null
          })
      }
    },
  },
  mounted() {
    this.fetchPurchasesSummary()
    this.fetchLastAddedPurchase()
  },
}
</script>

<style scoped>
.overlay {
  background: #f5f5fe;
  backdrop-filter: blur(7px);
  border: 1.5px dashed #000091;
  border-radius: 5px;
  color: #3a3a3a;
}
</style>
