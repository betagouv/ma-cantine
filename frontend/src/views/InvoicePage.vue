<template>
  <div>
    <div class="spinner" v-if="loading">
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </div>

    <div class="text-left">
      <v-btn text color="primary" class="ml-n4" :to="{ name: 'InvoicesHome' }" exact>
        <v-icon class="mr-2">mdi-arrow-left</v-icon>
        Revenir aux achats
      </v-btn>
    </div>

    <div class="text-left" v-if="purchase">
      <div v-if="isNewPurchase">
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Nouvel achat
        </h1>
      </div>
      <div v-else>
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Modifier mon achat
        </h1>
        <p>
          Vous pouvez modifier les données de cet achat dans le formulaire. Ces modifications seront visibles dans le
          diagnostic de la cantine choisie.
        </p>
      </div>

      <v-row v-if="purchase">
        <v-col cols="12" sm="8">
          <v-form ref="form" @submit.prevent v-model="formIsValid">
            <v-row>
              <v-col cols="12" sm="8">
                <label class="body-2" for="provider">Fournisseur</label>
                <v-text-field
                  validate-on-blur
                  hide-details="auto"
                  solo
                  v-model="purchase.provider"
                  class="mt-2"
                  id="provider"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <label class="body-2" for="price">Prix HT</label>
                <v-text-field
                  validate-on-blur
                  hide-details="auto"
                  solo
                  v-model="purchase.priceHt"
                  class="mt-2"
                  append-icon="mdi-currency-eur"
                  :rules="[validators.required]"
                  id="price"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="8" class="mb-6">
                <label class="body-2" for="canteen">Cantine</label>
                <v-autocomplete
                  hide-details
                  solo
                  :items="userCanteens"
                  placeholder="Choissisez la cantine"
                  v-model="purchase.canteen"
                  :rules="[validators.required]"
                  item-text="name"
                  item-value="id"
                  id="canteen"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <fieldset>
              <legend class="body-2 my-3">Catégorie</legend>
              <v-radio-group v-model="purchase.category" class="my-0">
                <v-radio class="ml-8" v-for="item in categories" :key="item" :label="item" :value="item">
                  <template v-slot:label>
                    <v-chip small :color="getCategoryDisplayValue(item).color" dark>
                      {{ getCategoryDisplayValue(item).text }}
                    </v-chip>
                  </template>
                </v-radio>
              </v-radio-group>
            </fieldset>

            <fieldset>
              <legend class="body-2 my-3">Caractéristique</legend>
              <v-row class="mb-4">
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                  class="py-0"
                  v-for="characteristic in characteristics"
                  :key="characteristic"
                >
                  <v-checkbox
                    hide-details="auto"
                    v-model="purchase.characteristics"
                    :multiple="true"
                    :key="characteristic"
                    :value="characteristic"
                    :label="getCharacteristicDisplayValue(characteristic).text"
                  />
                </v-col>
              </v-row>
            </fieldset>
          </v-form>
        </v-col>
        <v-col cols="12" md="4">
          <label class="body-2">Facture</label>

          <FilePreview
            v-model="purchase.invoiceFile"
            v-if="purchase.invoiceFile && typeof purchase.invoiceFile === 'string'"
            @delete="purchase.invoiceFile = null"
          ></FilePreview>

          <FileDrop
            v-else
            subtitle="Facture en PDF ou image acceptée"
            :acceptTypes="['image/jpeg, image/gif, image/png, application/pdf']"
            maxSize="10485760"
            :showUploadButton="false"
            @input="invoiceFileChanged = true"
            v-model="purchase.invoiceFile"
          />
        </v-col>
        <v-col cols="12">
          <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
            <v-spacer></v-spacer>
            <v-btn x-large outlined color="primary" class="mr-4 align-self-center" exact :to="{ name: 'InvoicesHome' }">
              Annuler
            </v-btn>
            <v-btn x-large color="primary" @click="savePurchase">
              Valider
            </v-btn>
          </v-sheet>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import FileDrop from "@/components/FileDrop"
import FilePreview from "@/components/FilePreview"
import { toBase64, getObjectDiff, normaliseText } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "InvoicePage",
  components: { FileDrop, FilePreview },
  data() {
    return {
      originalPurchase: null,
      bypassLeaveWarning: false,
      purchase: null,
      formIsValid: true,
      invoiceFileChanged: false,
      categories: ["VIANDES_VOLAILLES", "FRUITS_ET_LEGUMES", "PECHE", "PRODUITS_LAITIERS", "PRODUITS_TRANSFORMES"],
      characteristics: ["BIO", "AOCAOP", "RUP", "LABEL_ROUGE", "PECHE_DURABLE", "LOCAL", "HVE", "COMMERCE_EQUITABLE"],
    }
  },
  props: {
    id: {
      required: false,
    },
  },
  computed: {
    isNewPurchase() {
      return !this.id
    },
    validators() {
      return validators
    },
    hasChanged() {
      if (this.originalPurchase) {
        const diff = getObjectDiff(this.originalPurchase, this.purchase)
        return Object.keys(diff).length > 0
      } else {
        return Object.keys(this.purchase).length > 0
      }
    },
    loading() {
      return this.$store.state.purchasesLoadingStatus === Constants.LoadingStatus.LOADING
    },
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
  },
  methods: {
    getCategoryDisplayValue(category) {
      switch (category) {
        case "VIANDES_VOLAILLES":
          return { text: "Viandes / volailles", color: "deep-orange darken-1" }
        case "FRUITS_ET_LEGUMES":
          return { text: "Fruits et légumes", color: "green darken-1" }
        case "PECHE":
          return { text: "Pêche", color: "light-blue darken-1" }
        case "PRODUITS_LAITIERS":
          return { text: "Produits laitiers", color: "lime darken-2" }
        case "PRODUITS_TRANSFORMES":
          return { text: "Produits transformés", color: "deep-purple darken-1" }
        default:
          return { text: "Autre", color: "blue-grey darken-1" }
      }
    },
    getCharacteristicDisplayValue(characteristic) {
      switch (characteristic) {
        case "BIO":
          return { text: "Bio" }
        case "AOCAOP":
          return { text: "AOC / AOP" }
        case "RUP":
          return { text: "RUP" }
        case "LABEL_ROUGE":
          return { text: "Label Rouge" }
        case "PECHE_DURABLE":
          return { text: "Pêche Durable" }
        case "LOCAL":
          return { text: "Local" }
        case "HVE":
          return { text: "HVE" }
        case "COMMERCE_EQUITABLE":
          return { text: "Commerce Équitable" }
        default:
          return { text: "Autre" }
      }
    },
    async savePurchase() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      const payload = this.originalPurchase ? getObjectDiff(this.originalPurchase, this.purchase) : this.purchase

      if (this.invoiceFileChanged) {
        if (!this.purchase.invoiceFile) this.payload.invoiceFile = null
        else {
          const base64 = await new Promise((resolve, reject) => {
            toBase64(this.purchase.invoiceFile, resolve, reject)
          })
          this.$set(payload, "invoiceFile", base64)
        }
      }

      this.$store
        .dispatch(this.isNewPurchase ? "createPurchase" : "updatePurchase", {
          id: this.purchase.id,
          payload,
        })
        .then(() => {
          this.bypassLeaveWarning = true
          const message = this.isNewPurchase ? "Votre achat a bien été créée." : "Votre achat a bien été modifiée"
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message,
            status: "success",
          })
          this.$router.push({ name: "InvoicesHome" })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = "Quitter cette page ? Vos changements n'ont pas encore été sauvegardés"
      } else {
        delete e["returnValue"]
      }
    },
  },
  mounted() {
    if (this.purchase) return
    if (this.isNewPurchase) {
      this.purchase = {
        characteristics: [],
      }
      return
    }
    return fetch(`/api/v1/purchases/${this.id}`)
      .then((response) => {
        if (response.status !== 200) throw new Error()
        response.json().then((jsonPurchase) => {
          this.originalPurchase = jsonPurchase
          this.purchase = JSON.parse(JSON.stringify(jsonPurchase))
        })
      })
      .catch(() => {
        this.$store.dispatch("notify", {
          message: "Nous n'avons pas trouvé cet achat",
          status: "error",
        })
        this.$router.push({ name: "InvoicesHome" })
      })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
