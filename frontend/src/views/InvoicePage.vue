<template>
  <div>
    <div v-if="loading">
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </div>

    <div class="text-left">
      <router-link :to="{ name: 'InvoicesHome' }" exact class="mt-2 grey--text text--darken-1 caption">
        <v-icon small class="mr-2">mdi-arrow-left</v-icon>
        Revenir aux achats
      </router-link>
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
      </div>

      <v-row v-if="purchase">
        <v-col cols="12" md="8">
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
                  :rules="[validators.required, validators.greaterThanZero]"
                  id="price"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="8" class="mb-6">
                <label class="body-2" for="canteen">Cantine</label>
                <v-autocomplete
                  hide-details="auto"
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

              <v-col cols="12" sm="4">
                <label class="body-2" for="price">Date d'achat</label>

                <v-menu
                  v-model="menu"
                  :close-on-content-click="true"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      :value="humanReadableDate"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      :rules="[validators.required]"
                      v-on="on"
                      hide-details="auto"
                      solo
                      id="date"
                      class="mt-2"
                    ></v-text-field>
                  </template>

                  <v-date-picker v-model="purchase.date" :max="today" locale="fr-FR"></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
            <fieldset>
              <legend class="body-2 my-3">Catégorie</legend>
              <v-radio-group v-model="purchase.category" class="my-0">
                <div v-if="$vuetify.breakpoint.xs">
                  <v-radio
                    class="ml-8"
                    v-for="item in categories"
                    :key="item"
                    :label="getCategoryDisplayValue(item).text"
                    :value="item"
                  >
                    <template v-slot:label>
                      <span class="body-2 grey--text text--darken-3">{{ getCategoryDisplayValue(item).text }}</span>
                    </template>
                  </v-radio>
                </div>
                <v-row v-else>
                  <v-col>
                    <v-radio
                      class="ml-8"
                      v-for="item in [...categories.slice(0, Math.ceil(categories.length / 2))]"
                      :key="item"
                      :label="getCategoryDisplayValue(item).text"
                      :value="item"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ getCategoryDisplayValue(item).text }}</span>
                      </template>
                    </v-radio>
                  </v-col>
                  <v-col>
                    <v-radio
                      class="ml-8"
                      v-for="item in [...categories.slice(Math.ceil(categories.length / 2))]"
                      :key="item"
                      :label="getCategoryDisplayValue(item).text"
                      :value="item"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ getCategoryDisplayValue(item).text }}</span>
                      </template>
                    </v-radio>
                  </v-col>
                </v-row>
              </v-radio-group>
            </fieldset>

            <fieldset>
              <legend class="body-2 my-3">Caractéristiques</legend>
              <v-row class="mb-4">
                <v-col cols="12" sm="6" class="py-0" v-for="characteristic in characteristics" :key="characteristic">
                  <v-checkbox
                    hide-details="auto"
                    v-model="purchase.characteristics"
                    :multiple="true"
                    :key="characteristic"
                    :value="characteristic"
                    :label="getCharacteristicDisplayValue(characteristic).text"
                  >
                    <template v-slot:label>
                      <span class="body-2 grey--text text--darken-3">
                        {{ getCharacteristicDisplayValue(characteristic).text }}
                      </span>
                    </template>
                  </v-checkbox>
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
import { toBase64, getObjectDiff, normaliseText, formatDate } from "@/utils"
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
      menu: false,
      modal: false,
      categories: [
        "VIANDES_VOLAILLES",
        "PRODUITS_DE_LA_MER",
        "FRUITS_ET_LEGUMES",
        "PRODUITS_CEREALIERS",
        "ENTREES",
        "PRODUITS_LAITIERS",
        "BOISSONS",
        "AIDES",
        "BEURRE_OEUF_FROMAGE",
        "PRODUITS_SUCRES",
        "ALIMENTS_INFANTILES",
        "GLACES_SORBETS",
        "AUTRES",
      ],
      characteristics: [
        "BIO",
        "CONVERSION_BIO",
        "LABEL_ROUGE",
        "AOCAOP",
        "ICP",
        "STG",
        "HVE",
        "PECHE_DURABLE",
        "RUP",
        "FERMIER",
        "EQUIVALENTS",
        "COMMERCE_EQUITABLE",
        "EXTERNALITES",
        "PERFORMANCE",
      ],
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
    loading() {
      return this.$store.state.purchasesLoadingStatus === Constants.LoadingStatus.LOADING
    },
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
    humanReadableDate() {
      return this.purchase.date ? formatDate(this.purchase.date) : ""
    },
    today() {
      const today = new Date()
      return today.toISOString().split("T")[0]
    },
  },
  methods: {
    getCategoryDisplayValue(category) {
      const categoryHash = {
        VIANDES_VOLAILLES: { text: "Viandes, volailles", color: "red darken-4" },
        PRODUITS_DE_LA_MER: { text: "Produits de la mer", color: "pink darken-4" },
        FRUITS_ET_LEGUMES: { text: "Fruits, légumes, légumineuses et oléagineux", color: "purple darken-4" },
        PRODUITS_CEREALIERS: { text: "Produits céréaliers", color: "deep-purple darken-4" },
        ENTREES: { text: "Entrées et plats composés", color: "indigo darken-4" },
        PRODUITS_LAITIERS: { text: "Lait et produits laitiers", color: "blue darken-4" },
        BOISSONS: { text: "Boissons", color: "light-blue darken-4" },
        AIDES: { text: "Aides culinaires et ingrédients divers", color: "cyan darken-4" },
        BEURRE_OEUF_FROMAGE: { text: "Beurre, oeuf, fromage", color: "teal darken-4" },
        PRODUITS_SUCRES: { text: "Produits sucrés", color: "green darken-4" },
        ALIMENTS_INFANTILES: { text: "Aliments infantiles", color: "light-green darken-4" },
        GLACES_SORBETS: { text: "Glaces et sorbets", color: "blue-grey darken-4" },
        AUTRES: { text: "Autres", color: "brown darken-4" },
      }

      if (Object.prototype.hasOwnProperty.call(categoryHash, category)) return categoryHash[category]
      return { text: "", color: "" }
    },
    getCharacteristicDisplayValue(characteristic) {
      const characteristicHash = {
        BIO: { text: "Bio" },
        CONVERSION_BIO: { text: "En conversion bio" },
        LABEL_ROUGE: { text: "Label rouge" },
        AOCAOP: { text: "Appellation d'origine (AOC/AOP)" },
        ICP: { text: "Indication géographique protégée (IGP)" },
        STG: { text: "Spécialité traditionnelle garantie (STG)" },
        HVE: { text: "HVE ou certification environnementale de niveau 2" },
        PECHE_DURABLE: { text: "Pêche durable" },
        RUP: { text: "Région ultrapériphérique (RUP)" },
        FERMIER: { text: "Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »" },
        EXTERNALITES: {
          text:
            "Produits acquis prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
        },
        COMMERCE_EQUITABLE: { text: "Commerce équitable" },
        PERFORMANCE: { text: "Produits acquis sur la base de leurs performances en matière environnementale" },
        EQUIVALENTS: { text: "Produits équivalents aux produits bénéficiant de ces mentions ou labels" },
      }

      if (Object.prototype.hasOwnProperty.call(characteristicHash, characteristic))
        return characteristicHash[characteristic]
      return { text: "", color: "" }
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
    hasChanged() {
      if (this.originalPurchase) {
        const diff = getObjectDiff(this.originalPurchase, this.purchase)
        return Object.keys(diff).length > 0
      } else {
        return Object.keys(this.purchase).length > 0
      }
    },
    handleUnload(e) {
      if (this.hasChanged() && !this.bypassLeaveWarning) {
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
