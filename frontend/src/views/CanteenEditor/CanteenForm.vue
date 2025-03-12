<template>
  <div class="text-left">
    <h1 class="fr-h1">
      {{ isNewCanteen ? "Ajouter ma cantine" : "Modifier ma cantine" }}
    </h1>

    <TechnicalControlDialog
      :bodyText="technicalControlText"
      v-model="showTechnicalControlDialog"
      @save="(e) => saveCanteen(e, true)"
    />

    <div v-if="$route.query.etape === steps[0]">
      <h2 class="fr-h4">Étape 1/2 : Renseignez le SIRET de votre établissement</h2>
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

      <v-col v-if="isNewCanteen" sm="6" class="mt-12 px-0">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title><h2 class="fr-h5 mb-2">Besoin de créer plus de 5 cantines&nbsp;?</h2></v-card-title>
          <v-card-text>
            <p class="mb-0">
              Notre outil d'import permet de créer plusieurs cantines depuis un fichier tableur Excel, LibreOffice, ou
              CSV. Suivre les indications suivantes pour préparer votre fichier.
            </p>
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn :to="{ name: 'ImportCanteens' }" outlined color="primary">
              Importer mes cantines
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </div>

    <v-form v-else ref="form" v-model="formIsValid">
      <h2 class="fr-h4" v-if="isNewCanteen">Étape 2/2 : Compléter les informations</h2>
      <v-row>
        <v-col cols="12" sm="6">
          <p class="mb-2">SIRET</p>
          <p class="grey--text text--darken-2 d-flex align-center">
            {{ siret || canteen.siret }}
            <v-btn small @click="goToStep(0)" class="ml-2">Modifier</v-btn>
          </p>
        </v-col>
      </v-row>
      <v-row class="mt-0">
        <v-col cols="12" sm="6">
          <DsfrTextField
            hide-details="auto"
            label="Nom de la cantine"
            :rules="[validators.required]"
            validate-on-blur
            v-model="canteen.name"
            labelClasses="body-2 mb-2"
            aria-describedby="name-description"
          />
        </v-col>
        <v-col>
          <DsfrCallout id="name-description">
            <p class="ma-0 body-2">
              Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par
              exemple :
              <span class="font-italic">
                École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne...
              </span>
            </p>
          </DsfrCallout>
        </v-col>
      </v-row>
      <v-row class="mt-0">
        <v-col cols="12" sm="6">
          <CityField
            label="Ville"
            labelClasses="body-2 mb-2"
            :location="canteen"
            :rules="[validators.required]"
            @locationUpdate="setLocation"
          />
        </v-col>
      </v-row>

      <h3 class="fr-h5 mt-8 mb-2">Mon établissement est :</h3>
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrRadio
            label="Type d'établissement"
            labelClasses="body-2 mb-2 grey--text text--darken-4"
            :items="economicModels"
            v-model="canteen.economicModel"
            :rules="[validators.required]"
            aria-describedby="economicModel-description"
          />
          <DsfrRadio
            label="Mode de gestion"
            labelClasses="body-2 mb-2 grey--text text--darken-4"
            :items="managementTypes"
            v-model="canteen.managementType"
            :rules="[validators.required]"
          />
        </v-col>
        <v-col>
          <DsfrCallout id="economicModel-description">
            <p class="ma-0 body-2">
              <strong>Cantine publique</strong>
              : tout restaurant sous la responsabilité d’une personne morale de droit publique, qu’il soit opéré en
              gestion directe ou en gestion concédée (notamment avec une société de restauration collective privée). Les
              restaurants gérés par une association de gestion sont considérés comme publics dès lors que l’association
              de gestion est rattachée à une administration ou un établissement du secteur public (État, collectivité,
              fonction publique hospitalière)
            </p>
            <p class="ma-0 body-2">
              <strong>Cantine privée</strong>
              : restaurant sous la responsabilité d’une structure privée : entreprise, association (hors associations de
              gestion d’un restaurant de structure publique), établissement scolaire privé, etc.
            </p>
          </DsfrCallout>
        </v-col>
      </v-row>
      <v-row class="mt-0">
        <v-col cols="12">
          <DsfrRadio
            label="Mon établissement..."
            labelClasses="body-2 mb-2 grey--text text--darken-4"
            :items="productionTypes"
            v-model="canteen.productionType"
            :rules="[validators.required]"
          />
        </v-col>
      </v-row>
      <v-row class="mt-0">
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
            :hideOptional="true"
          />
        </v-col>

        <v-expand-transition>
          <v-col cols="12" md="8" v-if="usesCentralProducer" class="py-0">
            <DsfrTextField
              label="SIRET du livreur"
              labelClasses="body-2 mb-2"
              hide-details="auto"
              validate-on-blur
              v-model="canteen.centralProducerSiret"
              :rules="[
                validators.length(14),
                validators.luhn,
                validators.isDifferent(canteen.siret, satelliteSiretMessage),
                validators.required,
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
              du livreur.
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

      <h3 class="fr-h5 mt-8 mb-2">Mon établissement concerne :</h3>
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <DsfrNativeSelect
            label="Catégorie de secteur"
            labelClasses="body-2 mb-2"
            :items="sectorCategories"
            v-model="sectorCategory"
          />
        </v-col>
        <v-col cols="12" md="6">
          <div>
            <DsfrNativeSelect
              label="Secteurs d'activité"
              labelClasses="body-2 mb-2"
              :items="filteredSectors"
              v-model="chosenSector"
              item-text="name"
              item-value="id"
              no-data-text="Veuillez séléctionner la catégorie de secteur"
              :rules="canteen.sectors && canteen.sectors.length ? [] : [validators.required]"
            />
            <DsfrTagGroup :tags="sectorTags" :closeable="true" @closeTag="(tag) => removeSector(tag.id)" />
          </div>
        </v-col>
        <v-col v-if="showMinistryField" cols="12" md="10">
          <DsfrNativeSelect
            label="Administration générale de tutelle (ministère ou ATE)"
            hint="Hors fonction publique territoriale et hospitalière"
            labelClasses="body-2 mb-2"
            :items="ministries"
            v-model="canteen.lineMinistry"
            :rules="[validators.required]"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col>
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
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"
import { getObjectDiff, sectorsSelectList, readCookie, lineMinistryRequired } from "@/utils"
import TechnicalControlDialog from "./TechnicalControlDialog"
import SiretCheck from "./SiretCheck"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrRadio from "@/components/DsfrRadio"
import CityField from "./CityField"
import DsfrNativeSelect from "@/components/DsfrNativeSelect"
import DsfrCallout from "@/components/DsfrCallout"
import DsfrTagGroup from "@/components/DsfrTagGroup"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: {
    TechnicalControlDialog,
    DsfrTextField,
    DsfrRadio,
    CityField,
    DsfrNativeSelect,
    DsfrCallout,
    SiretCheck,
    DsfrTagGroup,
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
    const blankCanteen = { sectors: [] }
    return {
      siret: null,
      blankCanteen,
      canteen: JSON.parse(JSON.stringify(blankCanteen)),
      technicalControlText: null,
      showTechnicalControlDialog: false,
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      steps: ["siret", "informations-cantine"],
      satelliteSiretMessage: "Le numéro SIRET du livreur ne peut pas être le même que celui de la cantine satellite.",
      economicModels: Constants.EconomicModels,
      managementTypes: Constants.ManagementTypes,
      productionTypes: Constants.ProductionTypesDetailed.map((pt) => ({ text: pt.title, value: pt.value })),
      sectorCategory: null,
      chosenSector: null,
      ministries: this.$store.state.lineMinistries,
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
      return sectorsSelectList(this.sectors, this.sectorCategory).filter((s) => !s.header)
    },
    sectorCategories() {
      const displayValueMap = Constants.SectorCategoryTranslations
      const categoriesInUse = this.sectors.map((s) => s.category)
      const uniqueCategories = categoriesInUse.filter((c, idx) => categoriesInUse.indexOf(c) === idx)
      const categories = uniqueCategories.map((c) => ({ value: c, text: displayValueMap[c] }))
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
      return lineMinistryRequired(this.canteen, this.sectors)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    showDelete() {
      return !this.isNewCanteen && window.ENABLE_DASHBOARD
    },
    sectorTags() {
      return this.canteen.sectors.map((sectorId) => ({
        text: this.sectorName(sectorId),
        id: sectorId,
      }))
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
            `Vous êtes sur le point de déclarer une livraison depuis votre établissement à ${parseInt(
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
          const notify = () => {
            this.$store.dispatch("notify", {
              title: "Mise à jour prise en compte",
              message,
              status: "success",
            })
          }
          this.$emit("updateCanteen", canteenJson)
          if (this.isNewCanteen) {
            const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteenJson)

            let name = "DashboardManager"
            if (this.showSatelliteCanteensCount) name = "SatelliteManagement"

            this.$router
              .push({
                // form validation ensures that the count will be > 0
                name,
                params: { canteenUrlComponent },
              })
              .then(notify)
          } else {
            this.$router
              .push({
                name: "DashboardManager",
                params: {
                  canteenUrlComponent: this.canteenUrlComponent,
                },
              })
              .then(notify)
          }
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
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
      id = parseInt(id, 10) || id
      return this.sectors.find((s) => s.id === id)?.name || id
    },
    addSector(id) {
      id = +id
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
  watch: {
    chosenSector(newValue) {
      this.addSector(newValue)
    },
  },
}
</script>
