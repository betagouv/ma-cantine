<script setup>
import "@/css/dsfr-multi-select.css"
import { ref, reactive, computed } from "vue"
import { helpers } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"
import { useRootStore } from "@/stores/root"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import sectorsService from "@/services/sectors"
import openDataService from "@/services/openData.js"
import arraysService from "@/services/arrays.js"
import options from "@/constants/canteen-establishment-form-options"
import CanteenEstablishmentSearch from "@/components/CanteenEstablishmentSearch.vue"

/* Data */
const store = useRootStore()
const props = defineProps(["establishmentData", "showCreateButton", "showCancelButton", "addSatellite"])
const emit = defineEmits(["sendForm", "cancel"])

/* Siret */
const prefillEstablishment = ref(props.establishmentData)
const hasSiretOptions = computed(() => {
  let siretOptionWithDisabled = options.hasSiret
  siretOptionWithDisabled[1].disabled = form.productionType === "central" || form.productionType === "central_serving"
  return siretOptionWithDisabled
})

const changeHasSiret = () => {
  form.siret = null
  form.sirenUniteLegale = null
  form.postalCode = null
  form.citySelector = null
  form.city = null
  form.cityInseeCode = null
  form.department = null
  prefillEstablishment.value = null
  forceRerender.value++
  v$.value.$reset()
}

const selectEstablishment = (canteenInfos) => {
  switch (true) {
    case form.hasSiret === "has-siret":
      form.name = canteenInfos.name
      form.postalCode = canteenInfos.postalCode
      form.city = canteenInfos.city
      form.cityInseeCode = canteenInfos.cityInseeCode
      form.siret = canteenInfos.siret?.replace(" ", "")
      form.department = canteenInfos.department
      break
    case form.hasSiret === "no-siret":
      form.sirenUniteLegale = canteenInfos.siren?.replace(" ", "")
      break
  }
}

/* Production type */
const productionTypeOptions = computed(() => {
  const isDisabled = form.hasSiret === "no-siret"
  const disabledHint = isDisabled
    ? "Ce mode de production n'est pas disponible pour les établissements rattachés à une unité légale"
    : false
  const optionsWithDisabled = arraysService.createCopy(options.productionType)
  const indexCentralType = optionsWithDisabled.findIndex((option) => option.value === "central")
  const indexCentralServingType = optionsWithDisabled.findIndex((option) => option.value === "central_serving")
  optionsWithDisabled[indexCentralType].disabled = isDisabled
  optionsWithDisabled[indexCentralType].hint = disabledHint || optionsWithDisabled[indexCentralType].hint
  optionsWithDisabled[indexCentralServingType].disabled = isDisabled
  optionsWithDisabled[indexCentralServingType].hint = disabledHint || optionsWithDisabled[indexCentralType].hint
  return optionsWithDisabled
})

/* Sectors */
const sectorsOptions = ref([])
sectorsService.getSectors().then((sectors) => {
  const options = []
  for (let i = 0; i < sectors.length; i++) {
    const sector = sectors[i]
    const { name, value, categoryName, hasLineMinistry } = sector
    options.push({ name: name, sectorId: value, hasLineMinistry, hint: categoryName })
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

const getCitiesOptions = (callback) => {
  emptyCity.value = ""
  citiesOptions.value = []
  openDataService
    .findCitiesFromPostalCode(form.postalCode)
    .then((response) => {
      if (response.length === 0) emptyCity.value = `Aucune ville trouvée pour le code postal « ${form.postalCode} »`
      else displayCitiesResult(response)
      if (callback) callback()
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
const form = reactive({
  oneDelivery: null,
  manyDelivery: null,
  noSiret: null,
})

const resetFields = () => {
  form.hasSiret = null
  form.siret = null
  form.sirenUniteLegale = null
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

const prefillFields = () => {
  form.hasSiret = props.establishmentData.siret ? "has-siret" : "no-siret"
  form.siret = props.establishmentData.siret
  form.sirenUniteLegale = props.establishmentData.sirenUniteLegale
  form.name = props.establishmentData.name
  form.economicModel = props.establishmentData.economicModel
  form.managementType = props.establishmentData.managementType
  form.productionType = props.establishmentData.productionType
  form.sectors = props.establishmentData.sectors
  form.lineMinistry = props.establishmentData.lineMinistry
  form.dailyMealCount = props.establishmentData.dailyMealCount
  form.yearlyMealCount = props.establishmentData.yearlyMealCount
  form.centralProducerSiret = props.establishmentData.centralProducerSiret
  form.satelliteCanteensCount = props.establishmentData.satelliteCanteensCount
  form.postalCode = props.establishmentData.postalCode
  form.city = props.establishmentData.city
  form.cityInseeCode = props.establishmentData.cityInseeCode
  form.department = props.establishmentData.department
  getCitiesOptions(() => {
    form.citySelector = citiesOptions.value.findIndex(
      (option) => option.cityInseeCode === props.establishmentData.cityInseeCode
    )
  })
}

/* Dynamic Inputs */
const showCentralProducerSiret = computed(() => form.productionType === "site_cooked_elsewhere" && !props.addSatellite)
const showSatelliteCanteensCount = computed(
  () => form.productionType === "central" || form.productionType === "central_serving"
)
const showLineMinistry = computed(() => {
  if (sectorsOptions.value.length === 0) return false
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

const changeProductionMode = () => {
  form.satelliteCanteensCount = null
  form.centralProducerSiret = null
  form.sectors = []
  form.lineMinistry = null
  forceRerender.value++
}

/* Fields verification */
const { required, integer, minValue, maxValue, requiredIf, minLength, maxLength } = useValidators()
const productionTypeRequired = computed(() => !props.addSatellite)
const yearlyMealMinValue = computed(() => Math.max(form.dailyMealCount, 420))
const dailyMealMaxValue = computed(() => form.yearlyMealCount)
const siretIsRequired = computed(() => form.hasSiret === "has-siret")
const sirenIsRequired = computed(() => form.hasSiret === "no-siret")
const sectorsAreRequired = computed(() => form.productionType !== "central")

const rules = {
  name: { required },
  hasSiret: { required },
  siret: { required: requiredIf(siretIsRequired) },
  sirenUniteLegale: { required: requiredIf(sirenIsRequired) },
  citySelector: { required: requiredIf(showCitySelector) },
  postalCode: {
    required: requiredIf(showCitySelector),
    integer,
    minLength: helpers.withMessage("Le code postal doit contenir 5 caractères", minLength(5)),
    maxLength: helpers.withMessage("Le code postal doit contenir 5 caractères", maxLength(5)),
  },
  economicModel: { required },
  managementType: { required },
  productionType: { required: requiredIf(productionTypeRequired) },
  centralProducerSiret: {
    required: false,
    minLength: helpers.withMessage("Le SIRET doit contenir 14 caractères", minLength(14)),
    maxLength: helpers.withMessage("Le SIRET doit contenir 14 caractères", maxLength(14)),
  },
  sectors: {
    required: requiredIf(sectorsAreRequired),
    maxThree: helpers.withMessage(
      "Vous ne pouvez pas sélectionner plus de 3 secteurs",
      (sectors) => sectors.length <= 3
    ),
  },
  lineMinistry: { required: requiredIf(showLineMinistry) },
  dailyMealCount: { required, integer, minValue: minValue(3), maxValue: maxValue(dailyMealMaxValue) },
  yearlyMealCount: { required, integer, minValue: minValue(yearlyMealMinValue) },
  satelliteCanteensCount: { required: requiredIf(showSatelliteCanteensCount), integer, minValue: minValue(1) },
  oneDelivery: {
    beChecked: helpers.withMessage("La case doit être cochée", (value) => !showCheckboxOneDelivery.value || value),
  },
  manyDelivery: {
    beChecked: helpers.withMessage("La case doit être cochée", (value) => !showCheckboxManyDelivery.value || value),
  },
  noSiret: {
    beChecked: helpers.withMessage("La case doit être cochée", (value) => !showCheckboxNoSiret.value || value),
  },
}

/* Form */
const isSaving = ref(false)
const forceRerender = ref(0)
const v$ = useVuelidate(rules, form)

const validateForm = (action) => {
  v$.value.$validate()
  if (v$.value.$invalid) return
  emit("sendForm", { form: form, action: action })
}

/* Form fields initialisation */
if (props.establishmentData) {
  prefillFields()
  v$.value.$validate()
} else resetFields()
</script>

<template>
  <section
    class="canteen-establishment-form fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center"
  >
    <form class="fr-col-12 fr-col-lg-7 fr-background-default--grey fr-p-2w fr-p-md-7w" @submit.prevent="">
      <fieldset class="fr-mb-4w canteen-establishment-form__reduce-margin-bottom">
        <legend class="fr-h5 fr-mb-2w">1. Caractéristiques</legend>
        <DsfrRadioButtonSet
          legend="Modèle économique *"
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
          v-show="!addSatellite"
          legend="Mode de production *"
          v-model="form.productionType"
          :options="productionTypeOptions"
          :error-message="formatError(v$.productionType)"
          @change="changeProductionMode"
        />
        <DsfrInputGroup
          v-if="showCentralProducerSiret"
          v-model="form.centralProducerSiret"
          label="SIRET de la cuisine centrale"
          hint="Optionnel"
          :label-visible="true"
          :error-message="formatError(v$.centralProducerSiret)"
        />
        <DsfrInputGroup
          v-if="showSatelliteCanteensCount"
          v-model="form.satelliteCanteensCount"
          type="number"
          label="Nombre de restaurant satellite *"
          hint="Nombre de cantines/lieux de service à qui je fournis des repas"
          :label-visible="true"
          :error-message="formatError(v$.satelliteCanteensCount)"
        />
      </fieldset>
      <fieldset class="fr-mb-4w canteen-establishment-form__reduce-margin-bottom">
        <legend class="fr-h5 fr-mb-2w">2. Identification de l’établissement</legend>
        <DsfrRadioButtonSet
          v-model="form.hasSiret"
          legend="Avez-vous un numéro SIRET ?"
          :key="forceRerender"
          :error-message="formatError(v$.hasSiret)"
          :options="hasSiretOptions"
          @update:modelValue="changeHasSiret()"
        />
        <CanteenEstablishmentSearch
          v-if="form.hasSiret"
          :key="forceRerender"
          @select="(canteenInfos) => selectEstablishment(canteenInfos)"
          :error-required="formatError(v$.siret) || formatError(v$.sirenUniteLegale)"
          :has-siret="form.hasSiret === 'has-siret'"
          :establishment-data="prefillEstablishment"
        />
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">3. Coordonnées</legend>
        <DsfrInputGroup
          v-model="form.name"
          label="Nom de la cantine *"
          :label-visible="true"
          hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
          :error-message="formatError(v$.name)"
        />
        <div v-if="showCitySelector" class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.postalCode"
              label="Code postal *"
              hint="Indiquer le code postal pour pouvoir sélectionner une ville dans la liste"
              :label-visible="true"
              :error-message="formatError(v$.postalCode)"
              @update:modelValue="changePostal()"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrSelect
              class="fr-mb-0"
              v-model="form.citySelector"
              label="Ville *"
              description="Indiquer le code postal pour pouvoir sélectionner une ville dans la liste"
              :label-visible="true"
              :error-message="emptyCity || formatError(v$.citySelector)"
              :options="citiesOptions"
              @update:modelValue="selectCity()"
            />
          </div>
        </div>
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">4. Secteur</legend>
        <DsfrMultiselect
          v-if="form.productionType !== 'central'"
          v-model="form.sectors"
          label="Secteurs *"
          labelVisible
          hint="3 secteurs maximum"
          :options="sectorsOptions"
          search
          id-key="sectorId"
          label-key="name"
          @update:modelValue="resetLineMinistry()"
          :filtering-keys="['name']"
          :error-message="formatError(v$.sectors)"
        >
          <template #checkbox-label="{ option }">
            <div>
              <p class="fr-mb-0">{{ option.name }}</p>
              <p class="fr-mb-0 fr-hint-text">{{ option.hint }}</p>
            </div>
          </template>
        </DsfrMultiselect>
        <p v-else class="fr-mb-0">Concerne uniquement les cantines recevant des convives</p>
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
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.dailyMealCount"
              label="Par jour *"
              :label-visible="true"
              type="number"
              :error-message="formatError(v$.dailyMealCount)"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
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
          v-if="showCreateButton"
          :disabled="isSaving"
          :label="
            addSatellite
              ? 'Enregistrer et créer un nouveau restaurant satellite'
              : 'Enregistrer et créer un nouvel établissement'
          "
          secondary
          class="fr-mb-1v fr-mr-1v"
          @click="validateForm('stay-on-creation-page')"
        />
        <DsfrButton
          v-if="showCancelButton"
          :disabled="isSaving"
          label="Annuler"
          secondary
          class="fr-mb-1v fr-mr-1v"
          @click="emit('cancel')"
        />
        <DsfrButton
          :disabled="isSaving"
          label="Enregistrer"
          icon="fr-icon-save-line"
          @click="validateForm('go-to-canteen-page')"
        />
      </div>
    </form>
  </section>
</template>

<style lang="scss">
.canteen-establishment-form {
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
}
</style>
