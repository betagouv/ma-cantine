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
        <v-col cols="8" id="latest-purchases">
          <!-- How relevant are purchases to satellites? -->
          <v-card outlined>
            <v-card-title>Mes achats</v-card-title>
            <div v-if="purchases.length">
              <v-data-table class="px-4" :items="purchases" :headers="purchaseHeaders" />
              <v-card-actions>
                <v-btn :to="{ name: 'PurchasesHome' }" outlined color="primary" class="mx-2 mb-2">
                  Tous mes achats
                </v-btn>
              </v-card-actions>
            </div>
            <div v-else>
              <v-card-actions>
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
            <v-card-actions class="mx-2 mb-2">
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
          value: "date",
        },
        { text: "Produit", value: "description" },
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
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  mounted() {
    this.fetchCanteenIfNeeded()
  },
}
</script>
