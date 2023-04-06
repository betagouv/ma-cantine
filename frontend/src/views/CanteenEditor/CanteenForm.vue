<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" v-if="isNewCanteen" />
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCanteen ? "Ajouter ma cantine" : "Modifier ma cantine" }}
    </h1>

    <TechnicalControlDialog
      :bodyText="technicalControlText"
      v-model="showTechnicalControlDialog"
      @save="(e) => saveCanteen(e, true)"
    />

    <PublicationStateNotice
      :canteen="originalCanteen"
      :includeLink="true"
      v-if="!isNewCanteen && originalCanteen.productionType !== 'central'"
    />
    <div v-if="$route.query.etape === steps[0]">
      <h2 class="body-1 font-weight-bold mb-4">Étape 1/2 : Renseignez le SIRET de votre établissement</h2>
      <p>
        Vous ne le connaissez pas ? Utilisez
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
          l'Annuaire des Entreprises
          <v-icon color="primary" small>mdi-open-in-new</v-icon>
        </a>
        pour trouver le SIRET de votre cantine, ou
        <a href="https://annuaire-education.fr/" target="_blank" rel="noopener">
          l'Annuaire de l'Éducation
          <v-icon color="primary" small>mdi-open-in-new</v-icon>
        </a>
        pour les cantines scolaires.
      </p>

      <SiretCheck
        @siretIsValid="setSiret"
        :canteen="canteen"
        @updateCanteen="(x) => $emit('updateCanteen', x)"
        class="mt-10"
      />

      <p class="caption mb-n8">
        Pour toute question ou difficulté veuillez consulter notre
        <router-link :to="{ name: 'FaqPage' }">foire aux questions</router-link>
        ou
        <router-link :to="{ name: 'ContactPage' }">contactez-nous</router-link>
      </p>
    </div>

    <v-form v-else ref="form" v-model="formIsValid">
      <h2 class="mb-4" v-if="isNewCanteen">Étape 2/2 : Compléter les informations</h2>
      <v-row>
        <v-col cols="12" md="8">
          <p>SIRET</p>
          <p class="grey--text text--darken-2">
            {{ siret || canteen.siret }}
            <v-btn small @click="goToStep(0)">Modifier</v-btn>
          </p>
          <DsfrTextField
            hide-details="auto"
            label="Nom de la cantine"
            :rules="[validators.required]"
            validate-on-blur
            v-model="canteen.name"
            labelClasses="body-2 mb-2"
          />

          <p class="body-2 mt-4 mb-2">Ville</p>
          <DsfrAutocomplete
            hide-details="auto"
            :rules="[validators.required]"
            :loading="loadingCommunes"
            :items="communes"
            :search-input.sync="search"
            ref="cityAutocomplete"
            auto-select-first
            cache-items
            v-model="cityAutocompleteChoice"
            no-data-text="Pas de résultats. Veuillez renseigner votre ville"
          />
        </v-col>

        <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
          <label class="body-2" for="logo">
            Logo
          </label>
          <div v-if="canteen.logo" class="body-2 grey--text text--darken-1">
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
                  <v-icon aria-label="Supprimer logo" aria-hidden="false" color="red">$delete-line</v-icon>
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
          <p class="body-1 ml-1 mb-0">Mon établissement...</p>
          <v-radio-group
            class="mt-2"
            v-model="canteen.productionType"
            hide-details="auto"
            :rules="[validators.required]"
          >
            <v-radio class="ml-0" v-for="item in productionTypes" :key="item.value" :value="item.value">
              <template v-slot:label>
                <div class="d-block">
                  <div class="body-1 grey--text text--darken-4" v-html="item.title"></div>
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>

        <v-col cols="12" md="4" :class="showDailyMealCount ? '' : 'grey--text text--darken-1'">
          <label for="daily-meals" class="body-2 mb-2 d-block" :class="{ 'mb-lg-7': isNewCanteen }">
            Couverts moyen par
            <b>jour</b>
            (convives sur place)
          </label>
          <DsfrTextField
            id="daily-meals"
            hide-details="auto"
            :rules="showDailyMealCount ? [validators.greaterThanZero] : []"
            :disabled="!showDailyMealCount"
            :messages="showDailyMealCount ? [] : 'Concerne uniquement les cantines recevant des convives'"
            validate-on-blur
            v-model.number="canteen.dailyMealCount"
            prepend-icon="$restaurant-fill"
          />
        </v-col>

        <v-col cols="12" md="4">
          <label
            for="yearly-meals"
            class="body-2 d-block mb-2"
            :class="{
              'mb-lg-7': !showSatelliteCanteensCount,
            }"
          >
            Nombre total de couverts à
            <b>l'année</b>
            <span v-if="showSatelliteCanteensCount">&nbsp;(y compris les couverts livrés)</span>
          </label>
          <DsfrTextField
            id="yearly-meals"
            hide-details="auto"
            :rules="[validators.greaterThanZero, greaterThanDailyMealCount]"
            validate-on-blur
            v-model.number="canteen.yearlyMealCount"
            prepend-icon="$restaurant-fill"
          />
        </v-col>

        <v-col cols="12" md="4" :class="showSatelliteCanteensCount ? '' : 'grey--text text--darken-1'">
          <DsfrTextField
            label="Nombre de cantines/lieux de service à qui je fournis des repas"
            hide-details="auto"
            :rules="showSatelliteCanteensCount ? [validators.greaterThanZero] : []"
            :disabled="!showSatelliteCanteensCount"
            :messages="
              showSatelliteCanteensCount ? [] : 'Concerne uniquement les cuisines qui livrent à des satellites'
            "
            validate-on-blur
            v-model.number="canteen.satelliteCanteensCount"
            prepend-icon="$community-fill"
            labelClasses="body-2 mb-2"
          />
        </v-col>

        <v-expand-transition>
          <v-col cols="12" md="8" v-if="usesCentralProducer" class="py-0">
            <DsfrTextField
              label="SIRET de la cuisine centrale"
              class="mt-2"
              hide-details="auto"
              validate-on-blur
              v-model="canteen.centralProducerSiret"
              :rules="[
                validators.length(14),
                validators.luhn,
                validators.isDifferent(canteen.siret, satelliteSiretMessage),
              ]"
            />
            <p class="caption mt-1 ml-2">
              Vous ne le connaissez pas ? Utilisez cet
              <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
                outil de recherche pour trouver le SIRET
              </a>
              de la cuisine centrale.
            </p>
          </v-col>
        </v-expand-transition>
      </v-row>

      <v-row>
        <v-col cols="12" class="mt-4">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Secteurs d'activité</p>
            <DsfrSelect
              multiple
              :items="sectors"
              v-model="canteen.sectors"
              :rules="[validators.required]"
              item-text="name"
              item-value="id"
              hide-details="auto"
            />
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Type d'établissement</p>
            <DsfrSelect
              :items="economicModels"
              solo
              v-model="canteen.economicModel"
              :rules="[validators.required]"
              placeholder="Sélectionnez..."
              hide-details="auto"
              clearable
            />
          </div>
        </v-col>
        <v-col v-if="showMinistryField" cols="12">
          <p class="body-2">Ministère de tutelle</p>
          <DsfrSelect
            :items="ministries"
            v-model="canteen.lineMinistry"
            :rules="[validators.required]"
            placeholder="Sélectionnez le Ministère de tutelle"
            hide-details="auto"
            clearable
          />
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <p class="body-2 ml-4">Mode de gestion</p>
          <v-radio-group v-model="canteen.managementType" :rules="[validators.required]">
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
      <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
          Annuler
        </v-btn>
        <v-btn x-large color="primary" @click="saveCanteen">
          Valider
        </v-btn>
      </v-sheet>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"
import { toBase64, getObjectDiff, sectorsSelectList, readCookie, lastYear } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import TechnicalControlDialog from "./TechnicalControlDialog"
import ImagesField from "./ImagesField"
import SiretCheck from "./SiretCheck"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: {
    PublicationStateNotice,
    ImagesField,
    TechnicalControlDialog,
    DsfrTextField,
    DsfrAutocomplete,
    DsfrSelect,
    SiretCheck,
    BreadcrumbsNav,
  },
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
    const blankCanteen = { images: [], sectors: [] }
    return {
      siret: null,
      blankCanteen,
      canteen: JSON.parse(JSON.stringify(blankCanteen)),
      technicalControlText: null,
      showTechnicalControlDialog: false,
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      cityAutocompleteChoice: null,
      communes: [],
      loadingCommunes: false,
      search: null,
      managementTypes: Constants.ManagementTypes,
      steps: ["siret", "informations-cantine"],
      satelliteSiretMessage:
        "Le numéro SIRET de la cuisine centrale ne peut pas être le même que celui de la cantine satellite.",
      productionTypes: Constants.ProductionTypesDetailed,
      economicModels: Constants.EconomicModels,
      ministries: Constants.Ministries,
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
    isNewCanteen() {
      return !this.canteenUrlComponent
    },
    hasChanged() {
      const comparisonCanteen = this.originalCanteen || this.blankCanteen
      const diff = getObjectDiff(comparisonCanteen, this.canteen)
      return Object.keys(diff).length > 0
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    showDailyMealCount() {
      return this.canteen.productionType && this.canteen.productionType !== "central"
    },
    showMinistryField() {
      const concernedSectors = this.sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
  },
  beforeMount() {
    if (this.isNewCanteen) return

    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (canteen.city) {
        this.populateCityAutocomplete()
      }
      if (!this.canteen.images) this.canteen.images = []
    } else this.$router.push({ name: "NewCanteen" })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    if (this.originalCanteen) {
      document.title = `Modifier - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
    } else {
      document.title = `Ajouter ma cantine - ${this.$store.state.pageTitleSuffix}`
    }
    const step = this.siret || this.canteen?.siret || this.originalCanteen?.siret ? 1 : 0
    this.goToStep(step, false)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
    setSiret(siret) {
      this.siret = siret
      this.canteen.siret = this.siret
      this.goToStep(1)
    },
    goToStep(index, addHistory = true) {
      const params = { path: this.$route.path, query: { etape: this.steps[index] } }
      if (addHistory) this.$router.push(params).catch(() => {})
      else this.$router.replace(params).catch(() => {})
    },
    saveCanteen(e, bypassTechnicalControl = false) {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }

      const payload = this.originalCanteen ? getObjectDiff(this.originalCanteen, this.canteen) : this.canteen
      const fieldsToClean = ["dailyMealCount", "satelliteCanteensCount"]
      fieldsToClean.forEach((x) => {
        if (Object.prototype.hasOwnProperty.call(payload, x) && payload[x] === "") payload[x] = null
      })

      if (!bypassTechnicalControl) {
        if (this.canteen.productionType === "central_serving" && this.canteen.satelliteCanteensCount == 1) {
          this.displayTechnicalControlDialog("Est-ce que vous ne livrez vraiment qu'un seul autre site de service ?")
          return
        }
        const isCentralCanteen =
          this.canteen.productionType === "central_serving" || this.canteen.productionType === "central"
        if (isCentralCanteen && parseInt(this.canteen.satelliteCanteensCount) >= 250) {
          this.displayTechnicalControlDialog(
            `Vous êtes sur le point de déclarer une livraison depuis votre cuisine centrale à ${parseInt(
              this.canteen.satelliteCanteensCount
            )} établissements de service. Voulez-vous vraiment continuer ?`
          )
          return
        }
      }

      if (this.isNewCanteen) {
        for (let i = 0; i < Constants.TrackingParams.length; i++) {
          const cookieValue = readCookie(Constants.TrackingParams[i])
          if (cookieValue) payload[`creation_${Constants.TrackingParams[i]}`] = cookieValue
        }
      }

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
          this.$emit("updateCanteen", canteenJson)
          if (this.isNewCanteen) {
            const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteenJson)
            this.$router.push({
              // form validation ensures that the count will be > 0
              name: this.showSatelliteCanteensCount ? "SatelliteManagement" : "DiagnosticList",
              params: { canteenUrlComponent },
            })
          } else {
            // encourage TDs by redirecting to diagnostic page if relevant
            const diag = this.canteen.diagnostics.find((d) => d.year == lastYear())
            if (diag && diag.teledeclaration?.status !== "SUBMITTED") {
              this.$router.push({
                name: "DiagnosticModification",
                params: {
                  canteenUrlComponent: this.canteenUrlComponent,
                  year: lastYear(),
                },
              })
            } else {
              this.$router.push({ name: "ManagementPage" })
            }
          }
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
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
    populateCityAutocomplete() {
      const initialCityAutocomplete = {
        text: this.canteen.city,
        value: {
          label: this.canteen.city,
          citycode: this.canteen.cityInseeCode,
          postcode: this.canteen.postalCode,
          context: this.canteen.department,
        },
      }
      this.communes.push(initialCityAutocomplete)
      this.cityAutocompleteChoice = initialCityAutocomplete.value
    },
    displayTechnicalControlDialog(bodyText) {
      this.technicalControlText = bodyText
      this.showTechnicalControlDialog = true
    },
    greaterThanDailyMealCount(input) {
      if (input && this.canteen.productionType !== "central" && Number(input) < Number(this.canteen.dailyMealCount)) {
        return `Ce total doit être superieur du moyen de repas par jour sur place, actuellement ${this.canteen.dailyMealCount}`
      }
      return true
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
