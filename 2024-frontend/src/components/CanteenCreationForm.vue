<script setup>
import "@/css/dsfr-multi-select.css"
import { useRouter } from "vue-router"
import { ref, reactive, computed } from "vue"
import { helpers } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"
import { useRootStore } from "@/stores/root"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import sectorsService from "@/services/sectors"
import canteensService from "@/services/canteens"
import openDataService from "@/services/openData.js"
import options from "@/constants/canteen-creation-form-options"
import CanteenCreationSearch from "@/components/CanteenCreationSearch.vue"

/* Router and Store */
const router = useRouter()
const store = useRootStore()

/* Production type */
const productionTypeOptions = computed(() => {
  const isDisabled = form.hasSiret === "no-siret"
  const hint = isDisabled
    ? "Ce mode de production n'est pas disponible pour les établissements rattachés à une unité légale"
    : ""
  const optionsWithDisabled = [...options.productionType]
  const indexCentralType = optionsWithDisabled.findIndex((option) => option.value === "central")
  const indexCentralServingType = optionsWithDisabled.findIndex((option) => option.value === "central_serving")
  optionsWithDisabled[indexCentralType].disabled = isDisabled
  optionsWithDisabled[indexCentralType].hint = hint
  optionsWithDisabled[indexCentralServingType].disabled = isDisabled
  optionsWithDisabled[indexCentralServingType].hint = hint
  return optionsWithDisabled
})

/* Sectors */
const sectorsOptions = ref([])
sectorsService.getSectors().then((sectors) => {
  const options = []
  for (let i = 0; i < sectors.length; i++) {
    const sector = sectors[i]
    const { name, id, categoryName, hasLineMinistry } = sector
    options.push({ name: `${categoryName} - ${name}`, sectorId: id, hasLineMinistry })
  }
  const optionsSortedAlphabetically = options.sort((sectorBefore, sectorAfter) => {
    if (sectorBefore.name < sectorAfter.name) return -1
    else if (sectorBefore.name > sectorAfter.name) return 1
    else return 0
  })
  sectorsOptions.value = optionsSortedAlphabetically
})

/* Line Ministry */
const ministries = reactive({})
const lineMinistryOptions = computed(() => {
  if (!ministries.value) return []
  return ministries.value.map((lineMinistry) => {
    return { value: lineMinistry.value, text: lineMinistry.name }
  })
})
sectorsService.getMinistries().then((response) => {
  ministries.value = response
})
const resetLineMinistry = () => {
  form.lineMinistry = ""
}

/* City */
const defaultCitySelector = [
  {
    text: "Sélectionner une option",
    disabled: true,
    value: null,
  },
]
const emptyCity = ref("")
const citiesOptions = ref(defaultCitySelector)

const selectCity = () => {
  const index = Number(form.citySelector)
  const selectedCityOptions = citiesOptions.value[index]
  form.cityInseeCode = selectedCityOptions.cityInseeCode
  form.department = selectedCityOptions.department
  form.city = selectedCityOptions.text
}

const changePostal = () => {
  resetCity()
  if (form.postalCode && form.postalCode.trim().length === 5) getCitiesOptions()
}

const resetCity = () => {
  citiesOptions.value = defaultCitySelector
  form.citySelector = null
  form.city = null
  form.cityInseeCode = null
  form.department = null
}

const getCitiesOptions = () => {
  emptyCity.value = ""
  citiesOptions.value = []
  openDataService
    .findCitiesFromPostalCode(form.postalCode)
    .then((response) => {
      if (response.length === 0) emptyCity.value = `Aucune ville trouvée pour le code postal « ${form.postalCode} »`
      else displayCitiesResult(response)
    })
    .catch((e) => store.notifyServerError(e))
}

const displayCitiesResult = (cities) => {
  const options = []
  for (let i = 0; i < cities.length; i++) {
    const city = cities[i]
    options.push({
      value: i,
      text: city.nom,
      cityInseeCode: city.code,
      department: city.codeDepartement,
    })
  }
  citiesOptions.value = options
}

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.hasSiret = null
  form.siret = null
  form.name = null
  form.economicModel = null
  form.managementType = null
  form.productionType = null
  form.sectors = []
  form.lineMinistry = null
  form.dailyMealCount = null
  form.yearlyMealCount = null
  form.centralProducerSiret = null
  form.satelliteCanteensCount = null
  form.postalCode = null
  form.citySelector = null
  form.city = null
  form.cityInseeCode = null
  form.department = null
  form.oneDelivery = null
  form.manyDelivery = null
  form.noSiret = null
}
initFields()

/* Dynamic Inputs */
const hideDailyMealCount = computed(() => form.productionType === "central")
const showCentralProducerSiret = computed(() => form.productionType === "site_cooked_elsewhere")
const showSatelliteCanteensCount = computed(
  () => form.productionType === "central" || form.productionType === "central_serving"
)
const showLineMinistry = computed(() => {
  if (form.sectors.length === 0) return false
  if (form.economicModel !== "public") return false
  for (let i = 0; i < form.sectors.length; i++) {
    const index = sectorsOptions.value.findIndex((option) => option.sectorId === form.sectors[i])
    const sector = sectorsOptions.value[index]
    const hasLineMinistry = sector.hasLineMinistry
    if (hasLineMinistry) return true
  }
  return false
})
const showCheckboxOneDelivery = computed(() => Number(form.satelliteCanteensCount) === 1)
const showCheckboxManyDelivery = computed(() => Number(form.satelliteCanteensCount) >= 250)
const showCheckboxNoSiret = computed(() => form.hasSiret === "no-siret")
const showCitySelector = computed(() => form.hasSiret === "no-siret")

const resetDynamicInputValues = () => {
  form.satelliteCanteensCount = null
  form.centralProducerSiret = null
  form.dailyMealCount = null
}

/* Fields verification */
const { required, integer, minValue, requiredIf, minLength, maxLength } = useValidators()
const dailyMealRequired = computed(() => form.productionType !== "central")
const yearlyMealMinValue = computed(() => form.dailyMealCount || 0)
const rules = {
  name: { required },
  hasSiret: { required },
  siret: { required },
  citySelector: { required: requiredIf(showCitySelector) },
  postalCode: {
    required: requiredIf(showCitySelector),
    integer,
    minLength: helpers.withMessage("Le code postal doit contenir 5 caractères", minLength(5)),
    maxLength: helpers.withMessage("Le code postal doit contenir 5 caractères", maxLength(5)),
  },
  economicModel: { required },
  managementType: { required },
  productionType: { required },
  sectors: { required },
  lineMinistry: { required: requiredIf(showLineMinistry) },
  dailyMealCount: {
    required: requiredIf(dailyMealRequired),
    integer,
    minValue: minValue(0),
  },
  yearlyMealCount: { required, integer, minValue: minValue(yearlyMealMinValue) },
  satelliteCanteensCount: { required: requiredIf(showSatelliteCanteensCount), integer, minValue: minValue(0) },
  centralProducerSiret: {
    required: requiredIf(showCentralProducerSiret),
    notSameSiret: helpers.withMessage(
      "Le numéro SIRET du livreur ne peut pas être le même que celui de la cantine",
      (value) => value !== form.siret
    ),
    integer,
    minLength: helpers.withMessage("Le numéro SIRET doit contenir 14 caractères", minLength(14)),
    maxLength: helpers.withMessage("Le numéro SIRET doit contenir 14 caractères", maxLength(14)),
  },
  oneDelivery: {
    required: requiredIf(showCheckboxOneDelivery),
  },
  manyDelivery: {
    required: requiredIf(showCheckboxManyDelivery),
  },
  noSiret: {
    required: requiredIf(showCheckboxNoSiret),
  },
}
const v$ = useVuelidate(rules, form)
const validateForm = () => {
  v$.value.$validate()
  if (v$.value.$invalid) return
  sendCanteenForm()
}

/* Send Form */
const saveAndCreate = ref(false)
const isCreatingCanteen = ref(false)
const forceRerender = ref(0)

const saveCanteen = (saveAndCreateValue = false) => {
  saveAndCreate.value = saveAndCreateValue
  validateForm()
}

const sendCanteenForm = () => {
  const payload = form
  isCreatingCanteen.value = true
  canteensService
    .createCanteen(payload)
    .then((canteenCreated) => {
      if (canteenCreated.id && saveAndCreate.value) addNewCanteen(canteenCreated.name)
      else if (canteenCreated.id && !saveAndCreate.value) goToNewCanteenPage(canteenCreated.id)
      else {
        store.notifyServerError()
        isCreatingCanteen.value = false
      }
    })
    .catch((e) => {
      store.notifyServerError(e)
      isCreatingCanteen.value = false
    })
}

const goToNewCanteenPage = (id) => {
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: id },
  })
}

const addNewCanteen = (name) => {
  store.notify({ message: `Cantine ${name} créée avec succès.` })
  isCreatingCanteen.value = false
  saveAndCreate.value = false
  forceRerender.value++
  initFields()
  window.scrollTo(0, 0)
  v$.value.$reset()
}

/* Update canteen informations from child components */
const updateForm = (type, canteenInfos) => {
  if (type === "establishment") {
    form.siret = canteenInfos.siret?.replace(" ", "")
    form.name = canteenInfos.name
  }
  form.postalCode = canteenInfos.postalCode
  form.city = canteenInfos.city
  form.cityInseeCode = canteenInfos.cityInseeCode
  form.department = canteenInfos.department
}
</script>

<template>
  <section
    class="canteen-creation-form fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center"
  >
    <form class="fr-col-12 fr-col-lg-7 fr-background-default--grey fr-p-2w fr-p-md-7w" @submit.prevent="">
      <fieldset class="fr-mb-4w canteen-creation-form__reduce-margin-bottom">
        <legend class="fr-h5 fr-mb-2w">1. SIRET</legend>
        <DsfrRadioButtonSet
          v-model="form.hasSiret"
          legend="Avez-vous un numéro SIRET ?"
          :error-message="formatError(v$.hasSiret)"
          :options="options.hasSiret"
        />
        <CanteenCreationSearch
          v-if="form.hasSiret"
          :key="forceRerender"
          @select="
            (establishmentSelected) => {
              updateForm('establishment', establishmentSelected)
            }
          "
          :error-required="formatError(v$.siret)"
          :type="form.hasSiret"
        />
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">2. Coordonnées</legend>
        <DsfrInputGroup
          v-model="form.name"
          label="Nom de la cantine *"
          :label-visible="true"
          hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
          :error-message="formatError(v$.name)"
        />
        <div v-if="showCitySelector" class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-6">
            <DsfrInputGroup
              v-model="form.postalCode"
              label="Code postal *"
              :label-visible="true"
              :error-message="formatError(v$.postalCode)"
              @update:modelValue="changePostal()"
            />
          </div>
          <div class="fr-col-6">
            <DsfrSelect
              v-model="form.citySelector"
              label="Ville *"
              :label-visible="true"
              :error-message="emptyCity || formatError(v$.citySelector)"
              :options="citiesOptions"
              @update:modelValue="selectCity()"
            />
          </div>
        </div>
      </fieldset>
      <fieldset class="fr-mb-4w canteen-creation-form__reduce-margin-bottom">
        <legend class="fr-h5 fr-mb-2w">3. Caractéristiques</legend>
        <DsfrRadioButtonSet
          legend="Type d’établissement *"
          v-model="form.economicModel"
          :options="options.economicModel"
          :error-message="formatError(v$.economicModel)"
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion *"
          v-model="form.managementType"
          :options="options.managementType"
          :error-message="formatError(v$.managementType)"
        />
        <DsfrRadioButtonSet
          legend="Mode de production *"
          v-model="form.productionType"
          :options="productionTypeOptions"
          :error-message="formatError(v$.productionType)"
          @change="resetDynamicInputValues"
        />
        <div v-if="showCentralProducerSiret" class="canteen-creation-form__central-producer-siret">
          <DsfrInputGroup
            v-model="form.centralProducerSiret"
            label="SIRET du livreur *"
            :label-visible="true"
            :error-message="formatError(v$.centralProducerSiret)"
          />
          <p class="fr-hint-text fr-mb-0">
            Vous ne le connaissez pas ? Trouvez-le avec
            <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
          </p>
        </div>
        <DsfrInputGroup
          v-if="showSatelliteCanteensCount"
          v-model="form.satelliteCanteensCount"
          type="number"
          label="Nombre de cuisine satellite *"
          hint="Nombre de cantines/lieux de service à qui je fournis des repas"
          :label-visible="true"
          :error-message="formatError(v$.satelliteCanteensCount)"
        />
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">4. Secteur</legend>
        <DsfrMultiselect
          v-model="form.sectors"
          label="Secteurs *"
          labelVisible
          :options="sectorsOptions"
          search
          id-key="sectorId"
          label-key="name"
          @update:modelValue="resetLineMinistry()"
          :filtering-keys="['name']"
          :error-message="formatError(v$.sectors)"
        />
        <DsfrSelect
          v-if="showLineMinistry"
          v-model="form.lineMinistry"
          label="Administration générale de tutelle (ministère ou ATE) *"
          description="Hors fonction publique territoriale et hospitalière"
          labelVisible
          :options="lineMinistryOptions"
          :error-message="formatError(v$.lineMinistry)"
        />
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">5. Nombre de repas</legend>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-6">
            <DsfrInputGroup
              :class="{
                hide: hideDailyMealCount,
              }"
              v-model="form.dailyMealCount"
              :label="hideDailyMealCount ? 'Par jour' : 'Par jour *'"
              :label-visible="true"
              :disabled="hideDailyMealCount"
              :hint="hideDailyMealCount ? 'Concerne uniquement les cantines recevant des convives' : ''"
              type="number"
              :error-message="formatError(v$.dailyMealCount)"
            />
          </div>
          <div class="fr-col-6">
            <DsfrInputGroup
              v-model="form.yearlyMealCount"
              label="Par an *"
              :label-visible="true"
              type="number"
              :error-message="formatError(v$.yearlyMealCount)"
            />
          </div>
        </div>
      </fieldset>
      <fieldset
        v-if="showCheckboxOneDelivery || showCheckboxManyDelivery || showCheckboxNoSiret"
        class="fr-py-0 fr-my-3w fr-mb-md-3w"
      >
        <legend class="fr-h5 fr-mb-2w">6. Confirmation</legend>
        <DsfrCheckbox
          v-if="showCheckboxOneDelivery"
          v-model="form.oneDelivery"
          name="oneDelivery"
          label="En cochant cette case, je confirme déclarer une livraison depuis mon établissement à uniquement 1 seul autre site de service"
          :error-message="formatError(v$.oneDelivery)"
        />
        <DsfrCheckbox
          v-if="showCheckboxManyDelivery"
          v-model="form.manyDelivery"
          name="manyDelivery"
          :label="
            `En cochant cette case, je confirme déclarer une livraison depuis mon établissement à ${form.satelliteCanteensCount} sites de service`
          "
          :error-message="formatError(v$.manyDelivery)"
        />
        <div v-if="showCheckboxNoSiret">
          <p class="fr-mb-1v">
            Votre cantine n’a pas de numéro de SIRET et vous êtes sur le point de la rattacher à une unité légale
            existante. Avant de confirmer :
          </p>
          <ul>
            <li>
              avez-vous vérifié que votre cantine ne dispose pas d’un numéro SIRET (ex : une facture, l’annuaire des
              entreprises, annuaire des cantines scolaires) ?
            </li>
            <li>
              l’unité légale à laquelle vous vous rattachez correspond bien à l’entité qui contrôle votre cantine ?
            </li>
            <li>
              vous êtes-vous assuré que votre cantine ne figure pas dans la liste des établissements de l’unité légale ?
            </li>
          </ul>
          <p>
            Ces éléments sont essentiels pour éviter les doublons et garantir l’exactitude des télédéclarations
            effectuées sur ma cantine.
          </p>
          <DsfrCheckbox
            v-model="form.noSiret"
            name="noSiret"
            :error-message="formatError(v$.noSiret)"
            label="En cochant cette case vous confirmez avoir vérifié ces informations"
          />
        </div>
      </fieldset>
      <div class="fr-grid-row fr-grid-row--right fr-grid-row--top">
        <DsfrButton
          :disabled="isCreatingCanteen"
          label="Enregistrer et créer un nouvel établissement"
          secondary
          class="fr-mb-1v fr-mr-1v"
          @click="saveCanteen(true)"
        />
        <DsfrButton :disabled="isCreatingCanteen" label="Enregistrer" icon="fr-icon-save-line" @click="saveCanteen()" />
      </div>
    </form>
  </section>
</template>

<style lang="scss">
.canteen-creation-form {
  .hide {
    display: none !important;
  }

  &__reduce-margin-bottom {
    .fr-form-group:last-child {
      .fr-fieldset,
      .fr-fieldset__element:last-child {
        margin-bottom: 0 !important;
      }
    }
  }

  &__central-producer-siret {
    .fr-input-group {
      margin-bottom: 0.25rem !important;
    }
  }
}
</style>
