<template>
  <div class="text-left">
    <div v-if="loading">
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </div>

    <div>
      <BackLink :to="backLink" text="Revenir aux achats" />
    </div>

    <div v-if="purchase">
      <v-form ref="form" @submit.prevent v-model="formIsValid" v-if="purchase">
        <v-row>
          <v-col cols="12" md="8">
            <div v-if="isNewPurchase">
              <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
                Nouvelle facture
              </h1>
            </div>
            <div v-else>
              <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
                Modifier mon achat
              </h1>
            </div>
            <v-row class="mb-4">
              <v-col cols="12">
                <label class="body-2" for="provider">Fournisseur</label>
                <v-combobox
                  validate-on-blur
                  hide-details="auto"
                  solo
                  v-model="purchase.provider"
                  class="mt-2"
                  id="provider"
                  hide-no-data
                  :items="providers"
                  auto-select-first
                ></v-combobox>
              </v-col>

              <v-col cols="12" sm="8">
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
                  class="mt-2"
                  auto-select-first
                ></v-autocomplete>
              </v-col>

              <v-col cols="12" sm="4">
                <label class="body-2" for="date">Date d'achat</label>

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
              class="mt-2"
            />
          </v-col>
        </v-row>
        <h2 class="mb-4">Ajouter un produit</h2>
        <!-- TODO: data table with options for editing in dialog ? (but persistent form below for new ones) -->
        <v-row>
          <v-col cols="12" sm="8">
            <label class="body-2" for="description">Description</label>
            <v-combobox
              validate-on-blur
              hide-details="auto"
              solo
              v-model="purchase.description"
              class="mt-2"
              id="description"
              hide-no-data
              :items="productDescriptions"
              auto-select-first
            ></v-combobox>
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
          <v-col cols="12" sm="6">
            <label class="body-2" for="category">Categorie</label>
            <v-autocomplete
              validate-on-blur
              hide-details="auto"
              solo
              v-model="purchase.category"
              class="mt-2"
              id="category"
              hide-no-data
              :items="categories"
              auto-select-first
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="6">
            <label class="body-2" for="characteristic">Caractéristiques</label>
            <v-autocomplete
              validate-on-blur
              hide-details="auto"
              solo
              v-model="purchase.characteristics"
              class="mt-2"
              id="characteristic"
              hide-no-data
              :items="characteristics"
              auto-select-first
              multiple
            ></v-autocomplete>
          </v-col>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-btn
            :disabled="loading"
            x-large
            color="primary"
            @click="savePurchaseDemo(true)"
            v-if="isNewPurchase"
            class="ma-3 mt-6"
          >
            Valider
          </v-btn>
        </v-row>
        <v-expand-transition>
          <v-col cols="12" sm="6" v-show="showLocalDefinition" class="my-4">
            <label class="body-2" for="local-definition">C'est quoi votre définition de local ?</label>
            <v-autocomplete
              hide-details="auto"
              solo
              :items="localDefinitions"
              v-model="purchase.localDefinition"
              :rules="showLocalDefinition ? [validators.required] : []"
              id="local-definition"
              class="mt-2"
            ></v-autocomplete>
          </v-col>
        </v-expand-transition>
        <h2 class="my-4">Produits</h2>
        <v-data-table :headers="headers" :items="desserts" sort-by="calories">
          <template v-slot:[`item.actions`]>
            <v-icon small class="mr-2" @click="() => {}">
              mdi-pencil
            </v-icon>
            <v-icon small @click="() => {}">
              mdi-delete
            </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="() => {}">
              Reset
            </v-btn>
          </template>
        </v-data-table>
        <!-- <v-sheet
          rounded
          color="grey lighten-4 pa-3 mt-8"
          class="d-flex flex-column flex-sm-row align-start align-sm-center"
        >
          <v-dialog v-model="showDeleteDialog" v-if="!isNewPurchase" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn :disabled="loading" large v-bind="attrs" v-on="on" outlined color="error" class="ma-1">
                <v-icon class="mr-1">mdi-trash-can</v-icon>
                Supprimer
              </v-btn>
            </template>

            <v-card>
              <v-card-title class="font-weight-bold">Voulez-vous vraiment supprimer cet achat ?</v-card-title>

              <v-divider></v-divider>

              <v-card-actions class="pa-4">
                <v-spacer></v-spacer>
                <v-btn outlined text @click="showDeleteDialog = false" class="mr-2">
                  Non, revenir en arrière
                </v-btn>
                <v-btn outlined color="red" text @click="deletePurchase">
                  Oui, supprimer cet achat
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
          <v-btn
            :disabled="loading"
            x-large
            outlined
            color="primary"
            class="ma-1"
            exact
            :to="{ name: 'PurchasesHome' }"
          >
            Annuler
          </v-btn>
          <v-btn :disabled="loading" class="ma-1" x-large color="primary" @click="savePurchase()">
            Valider facture
          </v-btn>
        </v-sheet> -->
      </v-form>
    </div>
  </div>
</template>

<script>
import FileDrop from "@/components/FileDrop"
import FilePreview from "@/components/FilePreview"
import BackLink from "@/components/BackLink"
import { toBase64, getObjectDiff, normaliseText, formatDate } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "PurchasePage",
  components: { FileDrop, FilePreview, BackLink },
  data() {
    return {
      originalPurchase: null,
      bypassLeaveWarning: false,
      purchase: null,
      formIsValid: true,
      invoiceFileChanged: false,
      menu: false,
      modal: false,
      showDeleteDialog: false,
      categories: Object.values(Constants.Categories),
      characteristics: Object.values(Constants.Characteristics),
      backLink: { name: "PurchasesHome" },
      localDefinitions: [
        { text: "200 km autour du lieu de service", value: "AUTOUR_SERVICE" },
        { text: "Provenant du même département", value: "DEPARTMENT" },
        { text: "Provenant de la même région", value: "REGION" },
        { text: "Autre", value: "AUTRE" },
      ],
      productDescriptions: [],
      providers: [],
      desserts: [
        {
          name: "Frozen Yogurt",
          calories: 159,
          fat: "Lait et produits laitiers",
          carbs: "Bio, HVE",
        },
        {
          name: "Ice cream sandwich",
          calories: 237,
          fat: "Produits sucrés",
          carbs: "Local, Performance environnement...",
        },
      ],
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: "Produit",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Prix HT", value: "calories" },
        { text: "Catégorie", value: "fat" },
        { text: "Caractéristiques", value: "carbs" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      editedIndex: -1,
      editedItem: {
        name: "",
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
      defaultItem: {
        name: "",
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
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
    showLocalDefinition() {
      return this.purchase.characteristics.indexOf("LOCAL") > -1
    },
  },
  methods: {
    getCategoryDisplayText(category) {
      if (Object.prototype.hasOwnProperty.call(Constants.Categories, category))
        return Constants.Categories[category].text
      return ""
    },
    getCharacteristicDisplayText(characteristic) {
      if (Object.prototype.hasOwnProperty.call(Constants.Characteristics, characteristic))
        return Constants.Characteristics[characteristic].longText || Constants.Characteristics[characteristic].text
      return ""
    },
    async savePurchase(stayOnPage) {
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
          if (!stayOnPage) this.$router.push({ name: "PurchasesHome" })
          else {
            this.purchase = {
              characteristics: [],
            }
            this.$refs.form.resetValidation()
            this.fetchOptions() // if the user added a new product or provider, we need to refresh the options
          }
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    savePurchaseDemo() {
      this.desserts.push({
        name: this.purchase.description,
        calories: this.purchase.priceHt,
        fat: this.purchase.category,
        carbs: this.purchase.characteristics?.join(", "),
      })
      this.purchase.description = ""
      this.purchase.priceHt = null
      this.purchase.category = null
      this.purchase.characteristics = []
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
    deletePurchase() {
      this.$store
        .dispatch("deletePurchase", { id: this.purchase.id })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Votre achat a bien été supprimé",
            status: "success",
          })
          this.$router.push({ name: "PurchasesHome" })
          this.fetchOptions()
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    fetchOptions() {
      fetch("/api/v1/purchaseOptions/").then((response) => {
        if (response.status !== 200) throw new Error()
        response.json().then((options) => {
          this.productDescriptions = options.products
          this.providers = options.providers
        })
      }) // these lists are optional so don't bother with error messages if they fail to load
    },
  },
  mounted() {
    this.fetchOptions()
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
        this.$router.push({ name: "PurchasesHome" })
      })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (from.name == "PurchasesHome") {
        // keep filter settings in URL params
        vm.backLink = from
      }
    })
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
