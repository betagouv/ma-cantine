<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" v-if="isNewCanteen" />
    <h1 class="fr-h2 my-4">
      {{ isNewCanteen ? "Ajouter ma cantine" : "Modifier ma cantine" }}
    </h1>

    <TechnicalControlDialog
      :bodyText="technicalControlText"
      v-model="showTechnicalControlDialog"
      @save="(e) => saveCanteen(e, true)"
    />

    <div v-if="$route.query.etape === steps[0]">
      <h2 class="fr-h3 mb-4">Étape 1/2 : Renseignez le SIRET de votre établissement</h2>
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
        @siretIsValid="setCanteenData"
        :canteen="canteen"
        @updateCanteen="(x) => $emit('updateCanteen', x)"
        :backTo="{ name: 'ManagementPage' }"
        class="mt-10"
        ref="siret-check"
      />

      <p class="caption mb-n8">
        Pour toute question ou difficulté veuillez consulter notre
        <router-link :to="{ name: 'FaqPage' }">foire aux questions</router-link>
        ou
        <router-link :to="{ name: 'ContactPage' }">contactez-nous</router-link>
      </p>
    </div>

    <v-form v-else ref="form" v-model="formIsValid">
      <h2 class="fr-h3 mb-4" v-if="isNewCanteen">Étape 2/2 : Compléter les informations</h2>
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
            labelClasses="fr-text mb-2"
          />

          <p class="fr-text mt-4 mb-2">Ville</p>
          <CityField :location="canteen" :rules="[validators.required]" @locationUpdate="setLocation" />
        </v-col>

        <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
          <label class="fr-text" for="logo">
            Logo
          </label>
          <div v-if="canteen.logo" class="fr-text grey--text text--darken-1">
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
                <p class="ma-0 text-center font-weight-bold fr-text grey--text text--darken-2">Ajoutez un logo</p>
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
          <fieldset>
            <legend class="fr-text">Mon établissement...</legend>
            <v-radio-group
              class="mt-2"
              v-model="canteen.productionType"
              hide-details="auto"
              :rules="[validators.required]"
            >
              <v-radio class="ml-0" v-for="item in productionTypes" :key="item.value" :value="item.value">
                <template v-slot:label>
                  <div class="d-block">
                    <div class="fr-text grey--text text--darken-4" v-html="item.title"></div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </fieldset>
        </v-col>

        <v-col cols="12" md="4" :class="showDailyMealCount ? '' : 'grey--text text--darken-1'">
          <label for="daily-meals" class="fr-text mb-2 d-block">
            Couverts moyen par
            <b>jour</b>
            (convives sur place)
          </label>
          <DsfrTextField
            id="daily-meals"
            hide-details="auto"
            :rules="showDailyMealCount ? [validators.greaterThanZero, validators.isInteger] : []"
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
            class="fr-text d-block mb-2"
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
            :rules="[validators.greaterThanZero, validators.isInteger, greaterThanDailyMealCount]"
            validate-on-blur
            v-model.number="canteen.yearlyMealCount"
            prepend-icon="$restaurant-fill"
          />
        </v-col>

        <v-col cols="12" md="4" :class="showSatelliteCanteensCount ? '' : 'grey--text text--darken-1'">
          <DsfrTextField
            label="Nombre de cantines/lieux de service à qui je fournis des repas"
            hide-details="auto"
            :rules="showSatelliteCanteensCount ? [validators.greaterThanZero, validators.isInteger] : []"
            :disabled="!showSatelliteCanteensCount"
            :messages="
              showSatelliteCanteensCount ? [] : 'Concerne uniquement les cuisines qui livrent à des satellites'
            "
            validate-on-blur
            v-model.number="canteen.satelliteCanteensCount"
            prepend-icon="$community-fill"
            labelClasses="fr-text mb-2"
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
              @blur="getCentralKitchen"
            />
            <p class="caption mt-1 ml-2">
              Vous ne le connaissez pas ? Utilisez cet
              <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
                outil de recherche pour trouver le SIRET
                <v-icon x-small color="primary">mdi-open-in-new</v-icon>
              </a>
              de la cuisine centrale.
            </p>
            <v-expand-transition>
              <DsfrCallout v-if="centralKitchen && centralKitchen.id && centralKitchen.name">
                <p v-if="centralKitchen.isManagedByUser" class="mb-0">
                  Ce SIRET correspond à l'établissement que vous gérez
                  <router-link
                    :to="{
                      name: 'CanteenModification',
                      params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(centralKitchen) },
                    }"
                    target="_blank"
                  >
                    « {{ centralKitchen.name }} »
                    <v-icon small color="primary">mdi-open-in-new</v-icon>
                  </router-link>
                </p>
                <p v-else class="mb-0">Ce SIRET correspond à l'établissement « {{ centralKitchen.name }} »</p>
              </DsfrCallout>
            </v-expand-transition>
          </v-col>
        </v-expand-transition>
      </v-row>

      <v-row>
        <v-col cols="12" class="mt-4">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="8">
          <div>
            <p class="fr-text">Secteurs d'activité</p>
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
        <v-col v-if="showMinistryField" cols="12">
          <p class="fr-text">Ministère de tutelle</p>
          <DsfrSelect
            :items="ministries"
            v-model="canteen.lineMinistry"
            :rules="[validators.required]"
            placeholder="Sélectionnez le Ministère de tutelle"
            hide-details="auto"
            clearable
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <fieldset>
            <legend class="fr-text">Mode de gestion</legend>
            <v-radio-group class="mt-2" v-model="canteen.managementType" :rules="[validators.required]">
              <v-radio v-for="item in managementTypes" :key="item.value" :label="item.text" :value="item.value">
                <template v-slot:label>
                  <div class="d-block">
                    <div class="fr-text grey--text text--darken-4" v-html="item.text"></div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </fieldset>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <fieldset>
            <legend class="fr-text">Type d'établissement</legend>
            <v-radio-group class="mt-2" v-model="canteen.economicModel" :rules="[validators.required]">
              <v-radio v-for="item in economicModels" :key="item.value" :label="item.text" :value="item.value">
                <template v-slot:label>
                  <div class="d-block">
                    <div class="fr-text grey--text text--darken-4" v-html="item.text"></div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </fieldset>
        </v-col>
      </v-row>
      <div>
        <label class="fr-text" for="images">Images</label>
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
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrCallout from "@/components/DsfrCallout"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import CityField from "@/views/CanteenEditor/CityField"
import TechnicalControlDialog from "@/views/CanteenEditor/TechnicalControlDialog"
import ImagesField from "@/views/CanteenEditor/ImagesField"
import SiretCheck from "@/views/CanteenEditor/SiretCheck"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "StandaloneCanteenForm",
  components: {
    ImagesField,
    TechnicalControlDialog,
    DsfrTextField,
    CityField,
    DsfrSelect,
    DsfrCallout,
    SiretCheck,
    BreadcrumbsNav,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
  },
  data() {
    const blankCanteen = { images: [], sectors: [] }
    return {
      siret: null,
      blankCanteen,
      originalCanteen: null,
      canteen: JSON.parse(JSON.stringify(blankCanteen)),
      technicalControlText: null,
      showTechnicalControlDialog: false,
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      managementTypes: Constants.ManagementTypes,
      steps: ["siret", "informations-cantine"],
      satelliteSiretMessage:
        "Le numéro SIRET de la cuisine centrale ne peut pas être le même que celui de la cantine satellite.",
      productionTypes: Constants.ProductionTypesDetailed,
      economicModels: Constants.EconomicModels,
      ministries: Constants.Ministries,
      centralKitchen: null,
    }
  },
  computed: {
    canteenId() {
      return this.canteenUrlComponent.split("--")[0]
    },
    validators() {
      return validators
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
    isNewCanteen() {
      return !this.canteenUrlComponent || !this.originalCanteen
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
  mounted() {
    this.fetchCanteen().then(() => {
      if (this.isNewCanteen) {
        this.$router.push({ name: "NewCanteen", query: this.$route.query })
        document.title = `Ajouter ma cantine - ${this.$store.state.pageTitleSuffix}`
        return
      }
      const canteen = this.originalCanteen
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (!this.canteen.images) this.canteen.images = []
      this.getCentralKitchen()
      const step = this.siret || this.canteen?.siret || this.originalCanteen?.siret ? 1 : 0
      const queryParamsSiret = this.$route.query.siret
      this.goToStep(step, false)
      if (step === 0 && queryParamsSiret && !this.siret) {
        this.$nextTick(() => {
          this.$refs["siret-check"].siret = queryParamsSiret
          this.$nextTick(() => this.$refs["siret-check"].validateSiret())
        })
      }
      document.title = `Modifier - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
    })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
    fetchCanteen() {
      const id = this.canteenId
      return this.$store.dispatch("fetchCanteen", { id }).then((canteen) => {
        this.$set(this, "originalCanteen", canteen)
      })
    },
    setCanteenData(data) {
      this.siret = data.siret
      this.canteen.siret = this.siret
      if (!this.canteen.name) {
        this.canteen.name = data.name
      }
      if (!this.canteen.city) {
        this.canteen.city = data.city
        this.canteen.cityInseeCode = data.cityInseeCode
        this.canteen.postalCode = data.postalCode
        this.canteen.department = data.department
      }
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
              name: "DashboardManager",
              params: { canteenUrlComponent },
            })
          } else {
            // encourage TDs by redirecting to diagnostic page if relevant
            const diag = this.canteen.diagnostics.find((d) => d.year == lastYear())
            if (diag && diag.teledeclaration?.status !== "SUBMITTED") {
              this.$router.push({
                name: "MyProgress",
                params: {
                  canteenUrlComponent: this.canteenUrlComponent,
                  year: lastYear(),
                  measure: "etablissement",
                },
              })
            } else {
              this.$router.push({
                name: "DashboardManager",
                params: { canteenUrlComponent: this.canteenUrlComponent },
              })
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
    getCentralKitchen() {
      if (this.canteen.centralProducerSiret && this.canteen.siret !== this.canteen.centralProducerSiret) {
        fetch("/api/v1/canteenStatus/siret/" + this.canteen.centralProducerSiret)
          .then((response) => response.json())
          .then((response) => (this.centralKitchen = response))
      }
    },
    setLocation(location) {
      this.canteen.city = location.city
      this.canteen.cityInseeCode = location.cityInseeCode
      this.canteen.postalCode = location.postalCode
      this.canteen.department = location.department
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
