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
  const disabledHint = "Ce mode de production n'est pas disponible pour les établissements rattachés à une unité légale"
  const optionsWithDisabled = [...options.productionType]
  const indexCentralType = optionsWithDisabled.findIndex((option) => option.value === "central")
  const indexCentralServingType = optionsWithDisabled.findIndex((option) => option.value === "central_serving")
  optionsWithDisabled[indexCentralType].disabled = isDisabled
  optionsWithDisabled[indexCentralType].hint = isDisabled ? disabledHint : ""
  optionsWithDisabled[indexCentralServingType].disabled = isDisabled
  optionsWithDisabled[indexCentralServingType].hint = isDisabled ? disabledHint : ""
  return optionsWithDisabled
})

/* Sectors */
const sectors = reactive({})
const sectorsInCategory = computed(() => sectors.value.filter((sector) => sector.category === form.sectorCategory))
const sectorsCategoryOptions = computed(() => (sectors.value ? sectorsService.getCategories(sectors.value) : []))
const sectorsActivityOptions = computed(() =>
  sectors.value ? sectorsService.getActivities(sectorsInCategory.value) : []
)
sectorsService.getSectors().then((response) => {
  sectors.value = response
})
const changeCategory = () => {
  form.sectorActivity = []
  form.ministry = ""
  showMinistrySelector.value = false
}

/* Line Ministry */
const ministries = reactive({})
const showMinistrySelector = ref(false)
const ministryOptions = computed(() => {
  if (!ministries.value) return []
  return ministries.value.map((ministry) => {
    return { value: ministry.value, text: ministry.name }
  })
})
sectorsService.getMinistries().then((response) => {
  ministries.value = response
})
const verifyLineMinistry = () => {
  if (form.economicModel === "private") {
    showMinistrySelector.value = false
    form.ministry = ""
    return
  }
  for (let i = 0; i < form.sectorActivity.length; i++) {
    const key = form.sectorActivity[i]
    const activity = sectorsActivityOptions.value[key]
    const hasLineMinistry = activity.hasLineMinistry
    if (!hasLineMinistry) continue
    showMinistrySelector.value = true
    return
  }
}

/* City */
const citiesOptions = ref([{ value: "a", text: "Sélectionner une option", disabled: true }])
const changePostal = () => {
  if (form.city) form.city = ""
  if (form.postalCode && form.postalCode.trim().length === 5) getCitiesOptions()
}
const getCitiesOptions = () => {
  openDataService
    .getCities(form.postalCode)
    .then((response) => {
      const options = []
      for (let i = 0; i < response.length; i++) {
        const city = response[i]
        options.push({
          value: city.code,
          text: city.nom,
          inseeCode: city.code,
          department: city.codeDepartement,
        })
      }
      citiesOptions.value = options
    })
    .catch((e) => store.notifyServerError(e))
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
  form.sectorCategory = null
  form.sectorActivity = []
  form.ministry = null
  form.dailyMealCount = null
  form.yearlyMealCount = null
  form.centralProducerSiret = null
  form.satelliteCanteensCount = null
  form.postalCode = null
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
  city: { required: requiredIf(showCitySelector) },
  postalCode: {
    required: requiredIf(showCitySelector),
    integer,
    minLength: helpers.withMessage("Le code postal doit contenir 5 caractères", minLength(5)),
  },
  economicModel: { required },
  managementType: { required },
  productionType: { required },
  sectorCategory: { required },
  sectorActivity: { required },
  ministry: { required: requiredIf(showMinistrySelector) },
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
  payload.sectors = getSectorsID(form.sectorActivity)

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

const getSectorsID = (activitiesSelected) => {
  const names = []
  for (let i = 0; i < activitiesSelected.length; i++) {
    const index = activitiesSelected[i]
    names.push(sectorsActivityOptions.value[index].id)
  }
  return names
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
              v-model="form.city"
              label="Ville *"
              :label-visible="true"
              :error-message="formatError(v$.city)"
              :options="citiesOptions"
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
          @change="verifyLineMinistry()"
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
        <DsfrSelect
          v-model="form.sectorCategory"
          label="Catégorie de secteur *"
          labelVisible
          :options="sectorsCategoryOptions"
          @change="changeCategory()"
          :error-message="formatError(v$.sectorCategory)"
        />
        <DsfrMultiselect
          v-model="form.sectorActivity"
          label="Secteur d’activité *"
          labelVisible
          :options="sectorsActivityOptions"
          id-key="index"
          label-key="name"
          :filtering-keys="['name']"
          @change="verifyLineMinistry()"
          :error-message="formatError(v$.sectorActivity)"
        >
          <template #no-results>
            Sélectionner une catégorie de secteur pour pouvoir sélectionner des secteurs d'activité
          </template>
        </DsfrMultiselect>
        <DsfrSelect
          v-if="showMinistrySelector"
          v-model="form.ministry"
          label="Administration générale de tutelle (ministère ou ATE) *"
          description="Hors fonction publique territoriale et hospitalière"
          labelVisible
          :options="ministryOptions"
          :error-message="formatError(v$.ministry)"
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
              avez-vous vérifié que votre ne cantine ne dispose pas d’un numéro SIRET (ex : une facture, l’annuaire des
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
          <DsfrCheckbox v-model="form.noSiret" name="noSiret" :error-message="formatError(v$.noSiret)">
            <template #label>
              <p class="fr-mb-0">
                En cochant cette case vous confirmez avoir vérifié ces informations.
              </p>
            </template>
          </DsfrCheckbox>
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
