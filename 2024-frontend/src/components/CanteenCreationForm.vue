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
import options from "@/constants/canteen-creation-form-options"
import CanteenCreationSiret from "@/components/CanteenCreationSiret.vue"

/* Router and Store */
const router = useRouter()
const store = useRootStore()

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
  form.lineMinistry = ""
  showLineMinistrySelector.value = false
}

/* Line Ministry */
const lineMinistries = reactive({})
const showLineMinistrySelector = ref(false)
const lineMinistryOptions = computed(() => {
  if (!lineMinistries.value) return []
  return lineMinistries.value.map((lineMinistry) => {
    return { value: lineMinistry.value, text: lineMinistry.name }
  })
})
sectorsService.getMinistries().then((response) => {
  lineMinistries.value = response
})
const verifyLineMinistry = () => {
  if (form.economicModel === "private") {
    showLineMinistrySelector.value = false
    form.lineMinistry = ""
    return
  }
  for (let i = 0; i < form.sectorActivity.length; i++) {
    const key = form.sectorActivity[i]
    const activity = sectorsActivityOptions.value[key]
    const hasLineMinistry = activity.hasLineMinistry
    if (!hasLineMinistry) continue
    showLineMinistrySelector.value = true
  }
}

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.siret = null
  form.name = null
  form.economicModel = null
  form.managementType = null
  form.productionType = null
  form.sectorCategory = null
  form.sectorActivity = []
  form.lineMinistry = null
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
  siret: { required },
  economicModel: { required },
  managementType: { required },
  productionType: { required },
  sectorCategory: { required },
  sectorActivity: { required },
  lineMinistry: { required: requiredIf(showLineMinistrySelector) },
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

/* SIRET Informations */
const saveInfos = (canteenInfos) => {
  form.siret = canteenInfos.siret?.replace(" ", "")
  form.name = canteenInfos.name
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
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">1. SIRET</legend>
        <CanteenCreationSiret
          :key="forceRerender"
          @select="(canteenSelected) => saveInfos(canteenSelected)"
          :error-required="formatError(v$.siret)"
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
      </fieldset>
      <fieldset class="fr-mb-4w canteen-creation-form__caracteristics">
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
          :options="options.productionType"
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
          search
          selectAll
          :filtering-keys="['name']"
          @change="verifyLineMinistry()"
          :error-message="formatError(v$.sectorActivity)"
        >
          <template #no-results>
            Sélectionner une catégorie de secteur pour pouvoir sélectionner des secteurs d'activité
          </template>
        </DsfrMultiselect>
        <DsfrSelect
          v-if="showLineMinistrySelector"
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
      <fieldset v-if="showCheckboxOneDelivery || showCheckboxManyDelivery" class="fr-py-0 fr-my-3w fr-mb-md-3w">
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

  &__caracteristics {
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
