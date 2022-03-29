<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCanteen ? "Nouvelle cantine" : "Modifier ma cantine" }}
    </h1>

    <PublicationStateNotice
      :canteen="originalCanteen"
      :includeLink="true"
      v-if="!isNewCanteen && originalCanteen.productionType !== 'central'"
    />

    <v-form ref="form" v-model="formIsValid" lazy-validation>
      <v-row>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">Nom de la cantine</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.required]"
            validate-on-blur
            solo
            v-model="canteen.name"
          ></v-text-field>

          <p class="body-2 mt-4 mb-2">SIRET</p>
          <v-text-field
            hide-details="auto"
            validate-on-blur
            solo
            v-model="canteen.siret"
            :rules="[validators.length(14), validators.luhn]"
          ></v-text-field>

          <v-card outlined class="mt-2" v-if="duplicateSiretCanteen">
            <v-card-text class="red--text">
              <span v-if="duplicateSiretCanteen.id">
                Vous gérez déjà une cantine, « {{ duplicateSiretCanteen.name }} », avec ce SIRET et vous ne pouvez pas
                ajouter une autre cantine avec le même SIRET.
              </span>
              <span v-else>
                Une autre cantine, « {{ duplicateSiretCanteen.name }} », avec ce SIRET existe déjà dans notre système et
                vous ne pouvez pas ajouter une autre cantine avec le même SIRET.
                <br />
                <span class="grey--text">
                  Vouz pourriez contacter le gestionnaire de cette cantine pour demander à lui de vous ajouter dans
                  l'équipe de gestion.
                </span>
              </span>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                text
                :to="{
                  name: 'CanteenModification',
                  params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(duplicateSiretCanteen) },
                }"
                target="_blank"
                rel="noopener"
                v-if="duplicateSiretCanteen.id"
              >
                Aller à la cantine
              </v-btn>
              <v-btn color="primary" text @click="testfn" v-else>
                Envoyez le demande
              </v-btn>
              <v-dialog v-model="siretDialog" width="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn text v-bind="attrs" v-on="on">
                    Contactez-nous
                  </v-btn>
                </template>

                <v-card>
                  <v-card-title class="text-h5 grey lighten-2">
                    Contactez-nous
                  </v-card-title>
                  <v-form v-model="siretFormIsValid" ref="siretHelp" @submit.prevent class="pa-1 pa-md-4">
                    <v-text-field
                      v-model="siretHelpFromEmail"
                      label="Votre email"
                      :rules="[validators.email]"
                      validate-on-blur
                      outlined
                      class="my-2"
                    ></v-text-field>
                    <v-textarea
                      v-model="siretHelpMessage"
                      label="Message"
                      outlined
                      :rules="[validators.required]"
                      class="mt-2"
                    ></v-textarea>
                  </v-form>

                  <v-divider></v-divider>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn x-large outlined color="primary" @click="siretDialog = false" class="mr-2">
                      Annuler
                    </v-btn>
                    <v-btn x-large color="primary" @click="sendSiretHelp">
                      <v-icon class="mr-2">mdi-send</v-icon>
                      Envoyer
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-card-actions>
          </v-card>

          <p class="body-2 mt-4 mb-2">Ville</p>
          <v-autocomplete
            hide-details="auto"
            :rules="[validators.required]"
            :loading="loadingCommunes"
            :items="communes"
            :search-input.sync="search"
            ref="cityAutocomplete"
            solo
            auto-select-first
            cache-items
            v-model="cityAutocompleteChoice"
            :placeholder="canteen.city"
          ></v-autocomplete>
        </v-col>

        <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
          <label class="body-2" for="logo">
            Logo
          </label>
          <div v-if="canteen.logo" class="body-2 grey--text grey--lighten-2">
            Cliquez sur le logo pour changer
          </div>
          <div>
            <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onLogoChanged" id="logo" />
          </div>
          <div class="flex-grow-1 mt-2 fill-height">
            <v-card
              @click="onLogoUploadClick"
              rounded
              color="grey lighten-5"
              class="fill-height"
              style="overflow: hidden;"
              min-height="170"
            >
              <div v-if="canteen.logo" class="d-flex flex-column fill-height">
                <v-spacer></v-spacer>
                <v-img contain :src="canteen.logo" max-height="135"></v-img>
                <v-spacer></v-spacer>
              </div>
              <div v-else class="d-flex flex-column align-center justify-center fill-height">
                <v-icon class="pb-2">mdi-shape</v-icon>
                <p class="ma-0 text-center font-weight-bold body-2 grey--text text--darken-2">Ajoutez un logo</p>
              </div>
              <div v-if="canteen.logo" style="position: absolute; top: 10px; left: 10px;">
                <v-btn fab small @click.stop.prevent="changeLogo(null)">
                  <v-icon aria-label="Supprimer logo" aria-hidden="false" color="red">mdi-trash-can-outline</v-icon>
                </v-btn>
              </div>
            </v-card>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="mt-2">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12">
          <p class="body-1 ml-1 mb-0">Je suis...</p>
          <v-radio-group class="mt-2" v-model="canteen.productionType" hide-details="auto">
            <v-radio class="ml-0" v-for="item in productionTypes" :key="item.value" :value="item.value">
              <template v-slot:label>
                <div class="d-block">
                  <div class="body-1 grey--text text--darken-4" v-html="item.title"></div>
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>

        <v-col cols="12" md="6" v-if="showDailyMealCount">
          <p class="body-2 my-2">
            Couverts moyen par jour (convives sur place)
          </p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.greaterThanZero]"
            validate-on-blur
            solo
            v-model="canteen.dailyMealCount"
            prepend-icon="mdi-silverware-fork-knife"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6" v-if="showSatelliteCanteensCount">
          <p class="body-2 my-2">Nombre de cantines à qui je fournis des repas</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.greaterThanZero]"
            validate-on-blur
            solo
            v-model="canteen.satelliteCanteensCount"
            prepend-icon="mdi-home-city"
          ></v-text-field>
        </v-col>

        <v-col cols="12" class="mt-4">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Secteurs d'activité</p>
            <v-select
              multiple
              :items="sectors"
              solo
              v-model="canteen.sectors"
              item-text="name"
              item-value="id"
              hide-details
            ></v-select>
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Type d'établissement</p>
            <v-select
              :items="economicModels"
              solo
              v-model="canteen.economicModel"
              placeholder="Sélectionnez..."
              hide-details="auto"
              clearable
            ></v-select>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <p class="body-2 ml-4">Mode de gestion</p>
          <v-radio-group v-model="canteen.managementType">
            <v-radio
              class="ml-8"
              v-for="item in managementTypes"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            ></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>
      <div>
        <label class="body-2" for="images">Images</label>
        <ImagesField class="mt-0 mb-4" :imageArray.sync="canteen.images" id="images" />
      </div>
    </v-form>

    <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
        Annuler
      </v-btn>
      <v-btn x-large color="primary" @click="saveCanteen">
        Valider
      </v-btn>
    </v-sheet>
  </div>
</template>

<script>
import validators from "@/validators"
import { toBase64, getObjectDiff } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import ImagesField from "./ImagesField"
import Constants from "@/constants"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: { PublicationStateNotice, ImagesField },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
    originalCanteen: {
      type: Object,
      required: false,
    },
  },
  data() {
    const user = this.$store.state.loggedUser
    return {
      canteen: { images: [] },
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      cityAutocompleteChoice: {},
      communes: [],
      loadingCommunes: false,
      search: null,
      managementTypes: Constants.ManagementTypes,
      productionTypes: [
        {
          title: "une <b>cantine</b> qui produit sur place les repas que je sers à mes convives",
          body: "Je prépare ce que je sers à mes convives",
          value: "site",
        },
        {
          title: "une <b>cantine</b> qui sert des repas preparés par une cuisine centrale",
          body: "Les repas que je sers à mes convives sont cuisinés ailleurs",
          value: "site_cooked_elsewhere",
        },
        {
          title: "une <b>cuisine centrale</b> qui livre des satellites mais n'a pas de lieu de service en propre",
          body: "Je prépare des produits pour des cantines satellites et je ne reçois pas de convives sur place",
          value: "central",
        },
        {
          title: "une <b>cuisine centrale</b> qui accueille aussi des convives sur place",
          body: "Je prépare des produits pour des cantines satellites et j'ai aussi de la restauration sur place",
          value: "central_serving",
        },
      ],
      economicModels: [
        { text: "Public", value: "public" },
        { text: "Privé", value: "private" },
      ],
      // siret help
      siretFormIsValid: true,
      duplicateSiretCanteen: null,
      siretDialog: false,
      siretHelpFromEmail: user.email,
      siretHelpMessage: "",
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    isNewCanteen() {
      return !this.canteenUrlComponent
    },
    hasChanged() {
      if (this.originalCanteen) {
        const diff = getObjectDiff(this.originalCanteen, this.canteen)
        return Object.keys(diff).length > 0
      } else {
        return Object.keys(this.canteen).length > 0
      }
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    showDailyMealCount() {
      return this.canteen.productionType !== "central"
    },
  },
  beforeMount() {
    if (this.isNewCanteen) return

    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (canteen.city) {
        const initialCityAutocomplete = {
          text: canteen.city,
          value: {
            label: canteen.city,
            citycode: canteen.cityInseeCode,
            postcode: canteen.postalCode,
            context: canteen.department,
          },
        }
        this.communes = [initialCityAutocomplete]
        this.cityAutocompleteChoice = initialCityAutocomplete.value
      }
      if (!this.canteen.images) this.canteen.images = []
    } else this.$router.push({ name: "NewCanteen" })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    if (this.originalCanteen) {
      document.title = `Modifier - ${this.originalCanteen.name} - ma-cantine.beta.gouv.fr`
    } else {
      document.title = `Nouvelle cantine - ma-cantine.beta.gouv.fr`
    }
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
    saveCanteen() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = this.originalCanteen ? getObjectDiff(this.originalCanteen, this.canteen) : this.canteen
      this.$store
        .dispatch(this.isNewCanteen ? "createCanteen" : "updateCanteen", {
          id: this.canteen.id,
          payload,
        })
        .then((canteenJson) => {
          this.bypassLeaveWarning = true
          const message = this.isNewCanteen
            ? "Votre cantine a bien été créée. Vous pouvez maintenant ajouter des diagnostics."
            : "Votre cantine a bien été modifiée"
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message,
            status: "success",
          })
          if (this.isNewCanteen) {
            const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteenJson)
            this.$router.push({
              name: "DiagnosticList",
              params: { canteenUrlComponent },
            })
          } else {
            this.$router.push({ name: "ManagementPage" })
          }
        })
        .catch((e) => {
          if (e.jsonPromise) {
            e.jsonPromise.then((json) => {
              this.duplicateSiretCanteen = json
              this.siretHelpMessage = `Je veux ajouter une deuxième cantine avec le même SIRET : ${payload.siret}. (Ajoutez plus de détail)`
            })
            this.$store.dispatch("notifyRequiredFieldsError")
          } else {
            this.$store.dispatch("notifyServerError", e)
          }
        })
    },
    onLogoUploadClick() {
      this.$refs.uploader.click()
    },
    onLogoChanged(e) {
      this.changeLogo(e.target.files[0])
    },
    changeLogo(file) {
      if (!file) {
        this.canteen.logo = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.canteen, "logo", base64)
      })
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = LEAVE_WARNING
      } else {
        delete e["returnValue"]
      }
    },
    queryCommunes(val) {
      this.loadingCommunes = true
      const queryUrl = "https://api-adresse.data.gouv.fr/search/?q=" + val + "&type=municipality&autocomplete=1"
      return fetch(queryUrl)
        .then((response) => response.json())
        .then((response) => {
          const communes = response.features
          this.communes = communes.map((commune) => {
            return { text: `${commune.properties.label} (${commune.properties.context})`, value: commune.properties }
          })
          this.loadingCommunes = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    sendSiretHelp() {
      this.$refs.siretHelp.validate()
      if (!this.siretFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      let meta = this.meta || {}
      meta.userId = this.$store.state.loggedUser?.id
      meta.userAgent = navigator.userAgent

      const payload = {
        from: this.siretHelpFromEmail,
        // add in user name?
        message: this.siretHelpMessage,
        // TODO: if staying with trello, consider putting misc inquiry types in the title directly
        inquiryType: "cantine SIRET",
        meta,
      }

      this.$store
        .dispatch("sendInquiryEmail", payload)
        .then(() => {
          this.siretHelpFromMessage = ""
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.`,
          })
          this.siretDialog = false

          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
  watch: {
    search(val) {
      return val && val !== this.canteen.city && this.queryCommunes(val)
    },
    cityAutocompleteChoice(val) {
      if (val?.label) {
        this.canteen.city = val.label
        this.canteen.cityInseeCode = val.citycode
        this.canteen.postalCode = val.postcode
        this.canteen.department = val.context.split(",")[0]
      }

      this.search = this.canteen.city
    },
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged || this.bypassLeaveWarning) {
      next()
      return
    }
    window.confirm(LEAVE_WARNING) ? next() : next(false)
  },
}
</script>
