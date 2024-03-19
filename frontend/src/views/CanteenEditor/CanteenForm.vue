<template>
  <div class="text-left">
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
        <a
          href="https://annuaire-entreprises.data.gouv.fr/"
          target="_blank"
          rel="noopener external"
          title="l'Annuaire des Entreprises - ouvre une nouvelle fenêtre"
        >
          l'Annuaire des Entreprises
          <v-icon color="primary" small>mdi-open-in-new</v-icon>
        </a>
        pour trouver le SIRET de votre cantine, ou
        <a
          href="https://annuaire-education.fr/"
          target="_blank"
          rel="noopener external"
          title="l'Annuaire de l'Éducation - ouvre une nouvelle fenêtre"
        >
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
            aria-describedby="name-description"
          />

          <div class="mt-3 mb-6">
            <DsfrCallout>
              <p class="ma-0 body-2" id="name-description">
                Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par
                exemple :
                <span class="font-italic">
                  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne...
                </span>
              </p>
            </DsfrCallout>
          </div>

          <CityField
            label="Ville"
            labelClasses="body-2 mb-2"
            :location="canteen"
            :rules="[validators.required]"
            @locationUpdate="setLocation"
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
          <v-divider aria-hidden="true" role="presentation"></v-divider>
        </v-col>

        <v-col cols="12">
          <DsfrRadio
            label="Mon établissement..."
            :items="productionTypes"
            v-model="canteen.productionType"
            :rules="[validators.required]"
            class="mt-2"
          />
        </v-col>

        <v-col cols="12" md="4" :class="showDailyMealCount ? '' : 'grey--text text--darken-1'">
          <label for="daily-meals" class="body-2 mb-2 d-block">
            Nombre moyen de couverts par
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
            class="body-2 d-block mb-2"
            :class="{
              'mb-md-7': !showSatelliteCanteensCount,
            }"
          >
            Nombre total de couverts par
            <b>an</b>
            <span v-if="showSatelliteCanteensCount">&nbsp;(y compris les couverts livrés)</span>
          </label>
          <DsfrTextField
            id="yearly-meals"
            hide-details="auto"
            :rules="[validators.isInteger, validators.greaterThanZero, greaterThanDailyMealCount]"
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
            labelClasses="body-2 mb-2"
          />
        </v-col>

        <v-expand-transition>
          <v-col cols="12" md="8" v-if="usesCentralProducer" class="py-0">
            <DsfrTextField
              label="SIRET de la cuisine centrale"
              labelClasses="body-2 mb-2"
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
              <a
                href="https://annuaire-entreprises.data.gouv.fr/"
                target="_blank"
                rel="noopener external"
                title="outil de recherche pour trouver le SIRET - ouvre une nouvelle fenêtre"
              >
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
                    :title="`${centralKitchen.name} - ouvre une nouvelle fenêtre`"
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
          <v-divider aria-hidden="true" role="presentation"></v-divider>
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <div>
            <DsfrSelect
              label="Catégorie de secteur"
              labelClasses="body-2 mb-2"
              clearable
              :items="sectorCategories"
              v-model="sectorCategory"
              hide-details="auto"
            />
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <div>
            <DsfrSelect
              label="Secteurs d'activité"
              labelClasses="body-2 mb-2"
              :items="filteredSectors"
              :rules="canteen.sectors && canteen.sectors.length ? [] : [validators.required]"
              @change="addSector"
              v-model="chosenSector"
              item-text="name"
              item-value="id"
              hide-details="auto"
              no-data-text="Veuillez séléctionner la catégorie de secteur"
            />
            <div class="d-flex flex-wrap mt-2">
              <p v-for="id in canteen.sectors" :key="id" class="mb-0">
                <v-chip
                  close
                  @click="removeSector(id)"
                  @click:close="removeSector(id)"
                  class="mr-1 mt-1"
                  color="primary"
                >
                  {{ sectorName(id) }}
                </v-chip>
              </p>
            </div>
          </div>
        </v-col>
        <v-col v-if="showMinistryField" cols="12" md="10">
          <DsfrSelect
            label="Ministère de tutelle"
            labelClasses="body-2 mb-2"
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
        <v-col cols="12" sm="6" md="3">
          <DsfrRadio
            label="Type d'établissement"
            :items="economicModels"
            v-model="canteen.economicModel"
            :rules="[validators.required]"
            class="mt-2"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <DsfrRadio
            label="Mode de gestion"
            :items="managementTypes"
            v-model="canteen.managementType"
            :rules="[validators.required]"
            class="mt-2"
          />
        </v-col>
      </v-row>
      <div>
        <label class="body-2" for="images">Images</label>
        <ImagesField class="mt-0 mb-4" :imageArray.sync="canteen.images" id="images" />
      </div>
      <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
        <v-btn v-if="showDelete" x-large outlined color="red" :to="{ name: 'CanteenDeletion' }">
          Supprimer
        </v-btn>
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
import { toBase64, getObjectDiff, sectorsSelectList, readCookie } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import TechnicalControlDialog from "./TechnicalControlDialog"
import ImagesField from "./ImagesField"
import SiretCheck from "./SiretCheck"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrRadio from "@/components/DsfrRadio"
import CityField from "./CityField"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrCallout from "@/components/DsfrCallout"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: {
    PublicationStateNotice,
    ImagesField,
    TechnicalControlDialog,
    DsfrTextField,
    DsfrRadio,
    CityField,
    DsfrSelect,
    DsfrCallout,
    SiretCheck,
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
      managementTypes: Constants.ManagementTypes,
      steps: ["siret", "informations-cantine"],
      satelliteSiretMessage:
        "Le numéro SIRET de la cuisine centrale ne peut pas être le même que celui de la cantine satellite.",
      productionTypes: Constants.ProductionTypesDetailed.map((pt) => ({ text: pt.title, value: pt.value })),
      economicModels: Constants.EconomicModels,
      sectorCategory: null,
      chosenSector: null,
      ministries: Constants.Ministries,
      centralKitchen: null,
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    filteredSectors() {
      if (!this.sectorCategory) return []
      return sectorsSelectList(this.sectors, this.sectorCategory)
    },
    sectorCategories() {
      const displayValueMap = Constants.SectorCategoryTranslations
      const categoriesInUse = this.sectors.map((s) => s.category)
      const categories = categoriesInUse.map((c) => ({ value: c, text: displayValueMap[c] }))
      categories.sort((a, b) => {
        if (a.value === "autres" && b.value === "inconnu") return 0
        else if (a.value === "autres") return 1
        else if (a.value === "inconnu") return 1
        else if (b.value === "autres") return -1
        else if (b.value === "inconnu") return -1
        return a.text.localeCompare(b.text)
      })
      return categories
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
      return this.canteen.sectors?.some((x) => concernedSectors.indexOf(x) > -1)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    showDelete() {
      return !this.isNewCanteen && window.ENABLE_DASHBOARD
    },
  },
  mounted() {
    if (this.$route.query && this.$route.query["valider"]) {
      this.$nextTick(() => {
        const message = "Merci de vérifier les champs en rouge ci dessous"
        const title = null
        if (!this.$refs.form.validate()) this.$store.dispatch("notify", { title, message, status })
      })
    }
  },
  beforeMount() {
    if (this.isNewCanteen) return

    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (!this.canteen.images) this.canteen.images = []
      this.getCentralKitchen()
    } else this.$router.push({ name: "NewCanteen", query: this.$route.query })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    if (this.originalCanteen) {
      document.title = `Modifier - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
    } else {
      document.title = `Ajouter ma cantine - ${this.$store.state.pageTitleSuffix}`
    }
    const step = this.siret || this.canteen?.siret || this.originalCanteen?.siret ? 1 : 0
    const queryParamsSiret = this.$route.query.siret
    this.goToStep(step, false)
    if (step === 0 && queryParamsSiret && !this.siret) {
      this.$nextTick(() => {
        this.$refs["siret-check"].siret = queryParamsSiret
        this.$nextTick(() => this.$refs["siret-check"].validateSiret())
      })
    }
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
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
      const params = {
        path: this.$route.path,
        query: { ...(this.$route.query || {}), ...{ etape: this.steps[index] } },
      }
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

            let name = "DashboardManager"
            if (this.showSatelliteCanteensCount) name = "SatelliteManagement"

            this.$router.push({
              // form validation ensures that the count will be > 0
              name,
              params: { canteenUrlComponent },
            })
          } else {
            this.$router.push({
              name: "DashboardManager",
              params: {
                canteenUrlComponent: this.canteenUrlComponent,
              },
            })
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
    sectorName(id) {
      return this.sectors.find((s) => s.id === id)?.name || id
    },
    addSector(id) {
      if (!id || id < 0) return
      if (!this.canteen.sectors) this.canteen.sectors = []
      if (this.canteen.sectors.indexOf(id) === -1) this.canteen.sectors.push(id)
      this.$nextTick(() => {
        this.chosenSector = null
      })
    },
    removeSector(id) {
      this.canteen.sectors?.splice(this.canteen.sectors?.indexOf(id), 1)
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
