<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PurchasesHome' } }]" />

    <div v-if="loading">
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </div>

    <div v-if="purchase">
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

      <v-form ref="form" @submit.prevent v-model="formIsValid" v-if="purchase">
        <v-row>
          <v-col cols="12" md="8">
            <v-row class="mb-4">
              <v-col cols="12">
                <label class="body-2" for="description">
                  Description du produit
                </label>
                <DsfrCombobox
                  validate-on-blur
                  hide-details="auto"
                  v-model="purchase.description"
                  class="mt-2"
                  id="description"
                  :items="productDescriptions"
                  :rules="[validators.required]"
                ></DsfrCombobox>
              </v-col>
              <v-col cols="12" sm="8">
                <label class="body-2" for="provider">
                  Fournisseur
                </label>
                <DsfrCombobox
                  validate-on-blur
                  hide-details="auto"
                  v-model="purchase.provider"
                  class="mt-2"
                  id="provider"
                  :items="providers"
                  :rules="[validators.required]"
                ></DsfrCombobox>
              </v-col>
              <v-col cols="12" sm="4">
                <label class="body-2" for="price">Prix HT</label>
                <DsfrTextField
                  validate-on-blur
                  hide-details="auto"
                  v-model.number="purchase.priceHt"
                  class="mt-2"
                  append-icon="mdi-currency-eur"
                  :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
                  id="price"
                />
              </v-col>

              <v-col cols="12" sm="8">
                <label class="body-2" for="canteen">Cantine</label>
                <DsfrAutocomplete
                  hide-details="auto"
                  :items="userCanteens"
                  placeholder="Choisissez la cantine"
                  v-model="purchase.canteen"
                  :rules="[validators.required]"
                  item-text="name"
                  item-value="id"
                  id="canteen"
                  class="mt-2"
                  auto-select-first
                  no-data-text="Pas de résultats"
                />
              </v-col>

              <v-col cols="12" sm="4">
                <label class="body-2" for="date">Date d'achat</label>

                <v-menu
                  v-model="menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <DsfrTextField
                      :value="humanReadableDate"
                      prepend-icon="$calendar-event-fill"
                      readonly
                      v-bind="attrs"
                      :rules="[validators.required]"
                      v-on="on"
                      hide-details="auto"
                      id="date"
                      class="mt-2"
                    />
                  </template>

                  <v-date-picker
                    v-model="purchase.date"
                    :max="today"
                    locale="fr-FR"
                    @change="menu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
            <DsfrRadio
              label="Famille de produit"
              v-model="purchase.family"
              :items="productFamilies"
              @change="familyChange"
              optionsRow
              labelClasses="body-2 my-3"
              optionClasses="body-2"
              validate-on-blur
              :rules="[validators.required]"
            />
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
          <fieldset class="mx-4">
            <legend class="body-2 my-3">Caractéristiques</legend>
            <v-row class="mb-4">
              <v-col cols="12" sm="4" class="py-0" v-for="characteristic in characteristics" :key="characteristic">
                <v-checkbox
                  hide-details="auto"
                  v-model="purchase.characteristics"
                  :multiple="true"
                  :key="characteristic"
                  :value="characteristic"
                  :disabled="disabledForFamily(characteristic)"
                >
                  <template v-slot:label>
                    <span
                      :class="
                        `body-2 grey--text ${disabledForFamily(characteristic) ? 'text--darken-1' : 'text--darken-4'}`
                      "
                    >
                      {{ getCharacteristicDisplayText(characteristic) }}
                      <span v-if="disabledForFamily(characteristic)">
                        &nbsp;(non applicable)
                      </span>
                    </span>
                  </template>
                </v-checkbox>
              </v-col>
            </v-row>
          </fieldset>
        </v-row>
        <v-expand-transition>
          <v-col cols="12" sm="6" v-show="showLocalDefinition" class="my-4">
            <label class="body-2" for="local-definition">C'est quoi votre définition de local ?</label>
            <DsfrSelect
              hide-details="auto"
              :items="localDefinitions"
              v-model="purchase.localDefinition"
              :rules="showLocalDefinition ? [validators.required] : []"
              id="local-definition"
              class="mt-2"
              no-data-text="Pas de résultats"
            />
          </v-col>
        </v-expand-transition>
        <v-sheet
          rounded
          color="grey lighten-4 pa-3 mt-8"
          class="d-flex flex-column flex-sm-row align-start align-sm-center"
        >
          <v-dialog v-model="showDeleteDialog" v-if="!isNewPurchase" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn :disabled="loading" large v-bind="attrs" v-on="on" outlined color="red darken-2" class="ma-1">
                <v-icon class="mr-1">$delete-fill</v-icon>
                Supprimer
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <h1 class="fr-h6">Voulez-vous vraiment supprimer cet achat ?</h1>
              </v-card-title>

              <v-divider aria-hidden="true" role="presentation"></v-divider>

              <v-card-actions class="pa-4">
                <v-spacer></v-spacer>
                <v-btn outlined text @click="showDeleteDialog = false" class="mr-2">
                  Non, revenir en arrière
                </v-btn>
                <v-btn outlined color="red darken-2" text @click="deletePurchase">
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
            Valider
          </v-btn>
          <v-btn
            :disabled="loading"
            x-large
            color="primary"
            @click="savePurchase(true)"
            v-if="isNewPurchase"
            class="ma-1"
          >
            Valider et ajouter un nouveau
          </v-btn>
        </v-sheet>
      </v-form>
    </div>
  </div>
</template>

<script>
import FileDrop from "@/components/FileDrop"
import FilePreview from "@/components/FilePreview"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import { toBase64, getObjectDiff, normaliseText, formatDate } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrCombobox from "@/components/DsfrCombobox"
import DsfrRadio from "@/components/DsfrRadio"

export default {
  name: "PurchasePage",
  components: {
    FileDrop,
    FilePreview,
    BreadcrumbsNav,
    DsfrTextField,
    DsfrAutocomplete,
    DsfrSelect,
    DsfrCombobox,
    DsfrRadio,
  },
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
      productFamilies: Object.keys(Constants.ProductFamilies).map((f) => ({
        value: f,
        label: this.getProductFamilyDisplayText(f),
      })),
      characteristics: Object.keys(Constants.Characteristics),
      backLink: { name: "PurchasesHome" },
      localDefinitions: Object.values(Constants.LocalDefinitions),
      productDescriptions: [],
      providers: [],
      exceptions: Constants.CharacteristicFamilyExceptions,
      duplicating: this.$route.query.dupliquer,
    }
  },
  props: {
    id: {
      required: false,
    },
  },
  computed: {
    isNewPurchase() {
      return !this.id || this.duplicating
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
    getProductFamilyDisplayText(family) {
      if (Object.prototype.hasOwnProperty.call(Constants.ProductFamilies, family))
        return Constants.ProductFamilies[family].text
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
      const payload =
        this.originalPurchase && !this.duplicating ? getObjectDiff(this.originalPurchase, this.purchase) : this.purchase

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
          const message = this.isNewPurchase ? "Votre achat a bien été créé." : "Votre achat a bien été modifié"
          const notify = () => {
            this.$store.dispatch("notify", {
              title: "Mise à jour prise en compte",
              message,
              status: "success",
            })
          }
          if (!stayOnPage) this.$router.push({ name: "PurchasesHome" }).then(notify)
          else {
            this.purchase = {
              characteristics: [],
            }
            if (this.userCanteens.length === 1) {
              this.purchase.canteen = this.userCanteens[0].id
            }
            this.$refs.form.resetValidation()
            this.fetchOptions() // if the user added a new product or provider, we need to refresh the options
            window.scroll(0, 0)
            notify()
          }
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
    disabledForFamily(characteristic) {
      if (!this.purchase.family) return
      if (!this.exceptions[characteristic]) return
      return this.exceptions[characteristic].indexOf(this.purchase.family) > -1
    },
    familyChange() {
      this.$nextTick(() => {
        if (!this.purchase.family) return
        if (!this.purchase.characteristics) return
        const characteristicsToRemove = []
        this.purchase.characteristics.forEach((characteristic) => {
          if (!this.exceptions[characteristic]) return
          if (this.exceptions[characteristic].indexOf(this.purchase.family) > -1) {
            characteristicsToRemove.push(characteristic)
          }
        })
        characteristicsToRemove.forEach((char) => {
          const idx = this.purchase.characteristics.indexOf(char)
          this.purchase.characteristics.splice(idx, 1)
        })
      })
    },
  },
  mounted() {
    this.fetchOptions()
    if (this.purchase) return
    if (this.isNewPurchase && !this.duplicating) {
      this.purchase = {
        characteristics: [],
      }
      if (this.userCanteens.length === 1) {
        this.purchase.canteen = this.userCanteens[0].id
      }
      return
    }
    return fetch(`/api/v1/purchases/${this.id}`)
      .then((response) => {
        if (response.status !== 200) throw new Error()
        response.json().then((jsonPurchase) => {
          this.originalPurchase = jsonPurchase
          this.purchase = JSON.parse(JSON.stringify(jsonPurchase))
          if (this.duplicating) {
            this.purchase.id = null
            this.purchase.priceHt = null
            this.purchase.date = null
            this.purchase.invoiceFile = null
            this.purchase.importSource = "Duplication"
          }
        })
      })
      .catch(() => {
        this.$router.push({ name: "PurchasesHome" }).then(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cet achat",
            status: "error",
          })
        })
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
