<template>
  <div>
    <DsfrTextField
      hide-details="auto"
      label="Nom de la cantine"
      :rules="[validators.required]"
      validate-on-blur
      v-model="canteen.name"
      labelClasses="body-2 mb-2"
    />

    <!-- Possible to refactor to a different component. Not urgent. -->
    <p class="body-2 mt-5 mb-2">Ville</p>
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

    <p v-if="true || !canteen.productionType" class="body-1 ml-1 mt-5">Je suis...</p>
    <v-radio-group
      class="mt-2"
      v-if="true || !canteen.productionType"
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

    <label for="daily-meals" class="body-2 mb-2 mt-5 d-block" v-if="showDailyMealCount">
      Couverts moyen par
      <b>jour</b>
      (convives sur place)
    </label>
    <DsfrTextField
      id="daily-meals"
      type="number"
      hide-details="auto"
      :rules="[validators.greaterThanZero]"
      v-if="showDailyMealCount"
      validate-on-blur
      v-model="canteen.dailyMealCount"
      prepend-icon="$restaurant-fill"
    />

    <label for="yearly-meals" class="body-2 d-block mb-2 mt-5">
      Nombre total de couverts à
      <b>l'année</b>
      <span v-if="showSatelliteCanteensCount">&nbsp;(y compris les couverts livrés)</span>
    </label>
    <DsfrTextField
      id="yearly-meals"
      type="number"
      hide-details="auto"
      :rules="[validators.greaterThanZero, greaterThanDailyMealCount]"
      validate-on-blur
      v-model="canteen.yearlyMealCount"
      prepend-icon="$restaurant-fill"
    />

    <p class="body-2 mt-5">Mode de gestion</p>
    <v-radio-group v-model="canteen.managementType" :rules="[validators.required]">
      <v-radio
        class="ml-8"
        v-for="item in managementTypes"
        :key="item.value"
        :label="item.text"
        :value="item.value"
      ></v-radio>
    </v-radio-group>

    <p class="body-2">Secteurs d'activité</p>
    <DsfrSelect
      multiple
      :rules="[validators.required]"
      :items="sectors"
      v-model="canteen.sectors"
      item-text="name"
      item-value="id"
      hide-details
    />

    <p v-if="showMinistryField" class="body-2 mt-5">Ministère de tutelle</p>
    <DsfrSelect
      v-if="showMinistryField"
      :rules="[validators.required]"
      :items="ministries"
      v-model="canteen.lineMinistry"
      placeholder="Sélectionnez le Ministère de tutelle"
      hide-details="auto"
      clearable
    />

    <p class="body-2 mt-5">Type d'établissement</p>
    <DsfrSelect
      :items="economicModels"
      solo
      :rules="[validators.required]"
      v-model="canteen.economicModel"
      placeholder="Sélectionnez..."
      hide-details="auto"
      clearable
    />

    <DsfrTextField
      label="SIRET de la cuisine centrale"
      class="mt-2"
      hide-details="auto"
      validate-on-blur
      v-model="canteen.centralProducerSiret"
      v-if="usesCentralProducer"
      :rules="[
        validators.length(14),
        validators.luhn,
        validators.isDifferent(originalCanteen.siret, satelliteSiretMessage),
      ]"
    />
    <p class="caption mt-1 ml-2" v-if="usesCentralProducer">
      Vous ne le connaissez pas ? Utilisez cet
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
        outil de recherche pour trouver le SIRET
      </a>
      de la cuisine centrale.
    </p>

    <DsfrTextField
      label="Nombre de cantines/lieux de service à qui je fournis des repas"
      type="number"
      hide-details="auto"
      v-if="showSatelliteCanteensCount"
      :rules="[validators.greaterThanZero]"
      validate-on-blur
      v-model="canteen.satelliteCanteensCount"
      prepend-icon="$community-fill"
      labelClasses="body-2 mb-2"
    />
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import Constants from "@/constants"
import { sectorsSelectList } from "@/utils"

export default {
  props: {
    originalCanteen: {
      type: Object,
      required: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: { DsfrTextField, DsfrAutocomplete, DsfrSelect },
  data() {
    const blankCanteen = { images: [], sectors: [] }
    return {
      canteen: JSON.parse(JSON.stringify(blankCanteen)),
      loadingCommunes: false,
      communes: [],
      cityAutocompleteChoice: null,
      managementTypes: Constants.ManagementTypes,
      search: null,
      productionTypes: Constants.ProductionTypesDetailed,
      ministries: Constants.Ministries,
      economicModels: Constants.EconomicModels,
      satelliteSiretMessage:
        "Le numéro SIRET de la cuisine centrale ne peut pas être le même que celui de la cantine satellite.",
    }
  },
  computed: {
    validators() {
      return validators
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
    showMinistryField() {
      const concernedSectors = this.sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
    },
  },
  methods: {
    greaterThanDailyMealCount(input) {
      if (input && this.canteen.productionType !== "central" && Number(input) < Number(this.canteen.dailyMealCount)) {
        return `Ce total doit être superieur du moyen de repas par jour sur place, actuellement ${this.canteen.dailyMealCount}`
      }
      return true
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
    showDailyMealCount() {
      return this.canteen.productionType && this.canteen.productionType !== "central"
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
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
  beforeMount() {
    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (canteen.city) {
        this.populateCityAutocomplete()
      }
    }
  },
}
</script>
