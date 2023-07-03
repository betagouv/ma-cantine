<template>
  <div class="text-left">
    <h1 class="my-4 text-h5 font-weight-bold" v-if="canteen">{{ canteen.name }}</h1>
    <h1 class="my-4 text-h5 font-weight-bold" v-else>Bienvenue {{ loggedUser.firstName }}</h1>

    <h2 class="mt-8 mb-2 text-h6 font-weight-bold">
      Ma progression
    </h2>
    <p class="body-2">
      Vous trouverez ci-dessous une vue d'ensemble de votre progression sur les cinq volets de la loi EGAlim.
    </p>

    <div>
      <EgalimProgression v-if="hasProgression" />
      <EmptyProgression v-else />
    </div>

    <div v-if="canteen">
      <h2 class="mt-10 mb-2 text-h6 font-weight-bold">
        Mon établissement
      </h2>
      <p class="body-2">
        Accédez ci-dessous aux différents outils de gestion de votre établissement sur la plateforme « ma cantine ».
      </p>
      <v-row>
        <v-col cols="12" md="8" id="latest-purchases">
          <!-- How relevant are purchases to satellites? -->
          <v-card outlined>
            <v-card-title class="font-weight-bold">Mes achats</v-card-title>
            <div>
              <v-data-table
                class="px-4"
                :items="purchases"
                :headers="purchaseHeaders"
                :hide-default-header="true"
                :hide-default-footer="true"
                :disable-sort="true"
                no-data-text="Saisissez vos achats manuellement ou connectez votre logiciel de gestion habituel"
              >
                <template v-slot:[`item.characteristics`]="{ item }">
                  {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
                </template>
              </v-data-table>
              <v-card-actions class="justify-end" v-if="purchases.length">
                <v-btn :to="{ name: 'NewPurchase' }" outlined color="primary" class="mx-2 mb-2">
                  Ajouter un achat
                </v-btn>
                <v-btn :to="{ name: 'PurchasesImporter' }" outlined color="primary" class="mx-2 mb-2">
                  Importer des achats
                </v-btn>
                <v-btn :to="{ name: 'PurchasesHome' }" outlined color="primary" class="mx-2 mb-2">
                  Tous mes achats
                </v-btn>
              </v-card-actions>
              <v-card-actions class="justify-end" v-else>
                <v-btn :to="{ name: 'NewPurchase' }" outlined color="primary" class="mx-2 mb-2">
                  Ajouter mon premier achat
                </v-btn>
                <v-btn :to="{ name: 'PurchasesImporter' }" outlined color="primary" class="mx-2 mb-2">
                  Importer mes achats
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>
        <v-col cols="6" md="4" id="canteen-info-card">
          <v-card outlined>
            <v-card-title class="font-weight-bold">Mon établissement</v-card-title>
            <v-card-text>
              <p>SIRET : {{ canteen.siret }}</p>
              <div v-if="centralKitchen">
                <p>
                  La cuisine qui fournit les repas :
                  <router-link
                    :to="{
                      name: 'CanteenModification',
                      params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(centralKitchen) },
                    }"
                    target="_blank"
                    v-if="centralKitchen.isManagedByUser"
                  >
                    « {{ centralKitchen.name }} »
                    <v-icon small color="primary">mdi-open-in-new</v-icon>
                  </router-link>
                  <span v-else>« {{ centralKitchen.name }} »</span>
                </p>
              </div>
              <CanteenIndicators :canteen="canteen" />
            </v-card-text>
            <v-card-actions class="mx-2 mb-2 justify-end">
              <v-btn
                :to="{
                  name: 'CanteenForm',
                  params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                }"
                color="primary"
                outlined
              >
                Modifier
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="4" id="managers">
          <v-card outlined>
            <v-card-title class="font-weight-bold">
              Mon équipe
            </v-card-title>
            <v-card-text>
              <div v-if="managers.length > 1">
                <p>
                  {{ managers.length }} personnes (dont vous) peuvent actuellement modifier cet établissement et ajouter
                  des données
                </p>
                <ul class="pl-0">
                  <li v-for="(manager, idx) in managers" :key="manager.email">
                    <v-icon>
                      {{ manager.isInvite ? "mdi-account-clock-outline" : "mdi-account-check-outline" }}
                    </v-icon>
                    {{ manager.isInvite ? manager.email : `${manager.firstName} ${manager.lastName}` }}
                    <span v-if="idx === 0">(vous)</span>
                  </li>
                </ul>
              </div>
              <p v-else>
                Actuellement, vous êtes la seule personne qui peut modiifer cet établissement et ajouter des données
              </p>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                :to="{
                  name: 'CanteenManagers',
                  params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
                }"
                outlined
                color="primary"
                class="mx-2 mb-2"
              >
                Gérer mon équipe
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <h2 class="mt-10 mb-2 text-h6 font-weight-bold">
      Mes ressources personalisées
    </h2>
    <p class="body-2">
      Découvrez ci-dessous des articles et des outils pratiques, ainsi que des suggestions de partenaires et des
      cantines inspirantes sur votre territoire qui correspondent à vos enjeux.
    </p>
  </div>
</template>

<script>
import EmptyProgression from "./EmptyProgression.vue"
import EgalimProgression from "./EgalimProgression.vue"
import CanteenIndicators from "@/components/CanteenIndicators"
import { toCurrency } from "@/utils"
import Constants from "@/constants"

export default {
  name: "DashboardManager",
  components: { EmptyProgression, EgalimProgression, CanteenIndicators },
  data() {
    return {
      canteen: null,
      centralKitchen: null,
      purchases: [],
      purchaseHeaders: [
        {
          text: "Date",
          align: "start",
          value: "relativeDate",
        },
        { text: "Produit", value: "description" },
        { text: "Caractéristiques", value: "characteristics" },
        { text: "Prix HT", value: "priceHt", align: "end" },
      ],
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    hasProgression() {
      return false
    },
    canteenPreviews() {
      return this.$store.state.userCanteenPreviews
    },
    canteenId() {
      return this.canteenPreviews[0]?.id
    },
    managers() {
      if (!this.canteen) []
      const managersCopy = [...this.canteen.managers]
      const loggedUserIndex = managersCopy.findIndex((x) => x.email === this.$store.state.loggedUser.email)
      managersCopy.splice(0, 0, managersCopy.splice(loggedUserIndex, 1)[0])
      return managersCopy.concat(this.managerInvitations)
    },
    managerInvitations() {
      return (
        this.canteen?.managerInvitations.map((i) => {
          i.isInvite = true
          return i
        }) || []
      )
    },
  },
  methods: {
    fetchCanteenIfNeeded() {
      if (this.canteen) return
      const id = this.canteenId
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => {
          this.canteen = canteen
          this.getCentralKitchen()
          this.fetchPurchases()
        })
        .catch(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cette cantine",
            status: "error",
          })
        })
    },
    getCentralKitchen() {
      if (
        this.canteen &&
        this.canteen.centralProducerSiret &&
        this.canteen.siret !== this.canteen.centralProducerSiret
      ) {
        fetch("/api/v1/canteenStatus/siret/" + this.canteen.centralProducerSiret)
          .then((response) => response.json())
          .then((response) => (this.centralKitchen = response))
      }
    },
    fetchPurchases() {
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
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
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
      characteristics.splice(displayCount, Infinity)
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
    this.fetchCanteenIfNeeded()
  },
}
</script>

<style scoped>
ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
