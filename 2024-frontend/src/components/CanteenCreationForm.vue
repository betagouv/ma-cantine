<script setup>
import "@/css/dsfr-multi-select.css"
import { ref, reactive, computed } from "vue"
import { helpers } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import sectorsService from "@/services/sectors"
import { createCanteen } from "@/services/canteens"
import options from "@/constants/canteen-creation-form-options"

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

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.siret = ""
  form.name = ""
  form.economicModel = ""
  form.managementType = ""
  form.productionType = ""
  form.sectorCategory = ""
  form.sectorActivity = []
  form.ministry = ""
  form.dailyMealCount = ""
  form.yearlyMealCount = ""
  form.centralProducerSiret = ""
  form.satelliteCanteensCount = ""
}
initFields()

/* Dynamic Inputs */
const hideDailyMealCount = computed(() => form.productionType === "central")
const showCentralProducerSiret = computed(() => form.productionType === "site_cooked_elsewhere")
const showSatelliteCanteensCount = computed(
  () => form.productionType === "central" || form.productionType === "central_serving"
)

/* Fields verification */
const { required, integer, minValue, requiredIf, sameAs, not, minLength, maxLength } = useValidators()
const dailyMealRequired = computed(() => form.productionType !== "central")
const yearlyMealMinValue = computed(() => form.dailyMealCount || 0)
const rules = {
  name: { required },
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
  satelliteCanteensCount: { required: requiredIf(showCentralProducerSiret), integer, minValue: minValue(0) },
  centralProducerSiret: {
    required: requiredIf(showCentralProducerSiret),
    notSameSiret: helpers.withMessage(
      "Le numéro SIRET du livreur ne peut pas être le même que celui de la cantine",
      not(sameAs(form.siret))
    ),
    integer,
    minLength: helpers.withMessage("Le numéro SIRET doit contenir 14 caractères", minLength(14)),
    maxLength: helpers.withMessage("Le numéro SIRET doit contenir 14 caractères", maxLength(14)),
  },
}
const v$ = useVuelidate(rules, form)
const validateForm = () => {
  v$.value.$validate()
  if (v$.value.$invalid) return
  sendCanteenForm()
}

/* Send Form */
const sendCanteenForm = () => {
  const payload = {
    siret: "", // TODO à mettre en dynmaique ensuite
    postalCode: "73000", // TODO à mettre en dynmaique ensuite
    city: "Chambéry", // TODO à mettre en dynmaique ensuite
    cityInseeCode: "73065", // TODO à mettre en dynmaique ensuite
    department: "73", // TODO à mettre en dynmaique ensuite
    name: form.name,
    economicModel: form.economicModel,
    managementType: form.managementType,
    productionType: form.productionType,
    sectors: getSectorsID(form.sectorActivity),
    lineMinistry: form.ministry,
    dailyMealCount: Number(form.dailyMealCount),
    yearlyMealCount: Number(form.yearlyMealCount),
    centralProducerSiret: form.centralProducerSiret,
    satelliteCanteensCount: Number(form.satelliteCanteensCount),
  }

  createCanteen(payload).then((response) => {
    console.log("response", response)
  })
}

const getSectorsID = (activitiesSelected) => {
  const names = []
  for (let i = 0; i < activitiesSelected.length; i++) {
    const index = activitiesSelected[i]
    names.push(sectorsActivityOptions.value[index].id)
  }
  return names
}
</script>

<template>
  <section
    class="canteen-creation-form fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center"
  >
    <form class="fr-col-12 fr-col-md-7 fr-background-default--grey fr-p-2w fr-p-md-7w" @submit.prevent="validateForm()">
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">1. SIRET</legend>
      </fieldset>
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">2. Coordonnées</legend>
        <DsfrInputGroup
          v-model="form.name"
          label="Nom de la cantine"
          :label-visible="true"
          hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
          :error-message="formatError(v$.name)"
        />
      </fieldset>
      <fieldset class="fr-mb-3w">
        <legend class="fr-h5">3. Caractéristiques</legend>
        <DsfrRadioButtonSet
          legend="Type d’établissement"
          v-model="form.economicModel"
          :small="true"
          :options="options.economicModel"
          @change="verifyLineMinistry()"
          :error-message="formatError(v$.economicModel)"
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion"
          v-model="form.managementType"
          :small="true"
          :options="options.managementType"
          :error-message="formatError(v$.managementType)"
        />
        <DsfrRadioButtonSet
          legend="Mode de production"
          v-model="form.productionType"
          :small="true"
          :options="options.productionType"
          :error-message="formatError(v$.productionType)"
        />
        <div v-if="showCentralProducerSiret" class="canteen-creation-form__central-producer-siret">
          <DsfrInputGroup
            v-model="form.centralProducerSiret"
            label="SIRET du livreur"
            :label-visible="true"
            :error-message="formatError(v$.centralProducerSiret)"
          />
          <p class="fr-hint-text">
            Vous ne le connaissez pas ? Trouvez-le avec
            <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
          </p>
        </div>

        <DsfrInputGroup
          v-if="showSatelliteCanteensCount"
          v-model="form.satelliteCanteensCount"
          type="number"
          label="Nombre de cuisine satellite"
          hint="Nombre de cantines/lieux de service à qui je fournis des repas"
          :label-visible="true"
          :error-message="formatError(v$.satelliteCanteensCount)"
        />
      </fieldset>
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">4. Secteur</legend>
        <DsfrSelect
          v-model="form.sectorCategory"
          label="Catégorie de secteur"
          labelVisible
          :options="sectorsCategoryOptions"
          @change="changeCategory()"
          :error-message="formatError(v$.sectorCategory)"
        />
        <DsfrMultiselect
          v-model="form.sectorActivity"
          label="Secteur d’activité"
          labelVisible
          :options="sectorsActivityOptions"
          id-key="index"
          label-key="name"
          search
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
          label="Administration générale de tutelle (ministère ou ATE)"
          description="Hors fonction publique territoriale et hospitalière"
          labelVisible
          :options="ministryOptions"
          :error-message="formatError(v$.ministry)"
        />
      </fieldset>
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">5. Nombre de repas</legend>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-6">
            <DsfrInputGroup
              :class="{
                hide: hideDailyMealCount,
              }"
              v-model="form.dailyMealCount"
              label="Par jour"
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
              label="Par an"
              :label-visible="true"
              type="number"
              :error-message="formatError(v$.yearlyMealCount)"
            />
          </div>
        </div>
      </fieldset>
      <fieldset class="fr-py-0">
        <div class="fr-grid-row fr-grid-row--right">
          <DsfrButton label="Enregistrer" type="submmit" icon="fr-icon-save-line" />
        </div>
      </fieldset>
    </form>
  </section>
</template>

<style lang="scss">
.canteen-creation-form {
  .hide {
    display: none !important;
  }

  &__central-producer-siret {
    .fr-input-group {
      margin-bottom: 0.25rem !important;
    }
  }
}
</style>
