<script setup>
import { ref, reactive } from "vue"
import documentation from "@/data/documentation.json"
import options from "@/constants/canteen-form-options"
import CanteenEstablishmentSearch from "@/components/CanteenEstablishmentSearch.vue"

/* Data */
const props = defineProps(["establishmentData", "showCancelButton", "errors"])
const emit = defineEmits(["sendForm", "cancel"])
const prefillEstablishment = ref(props.establishmentData)

/* SIREN */
const selectEstablishment = (canteenInfos) => {
  form.sirenUniteLegale = canteenInfos.siren?.replace(" ", "")
}

/* FORM */
const form = reactive({
  productionType: "groupe", // TODO: remove hard coded value and use data file
})

const resetFields = () => {
  form.sirenUniteLegale = null
  form.name = null
  form.managementType = null
  form.dailyMealCount = null
  form.yearlyMealCount = null
  form.centralProducerSiret = null
}

const prefillFields = () => {
  form.sirenUniteLegale = props.establishmentData.sirenUniteLegale
  form.name = props.establishmentData.name
  form.managementType = props.establishmentData.managementType
  form.dailyMealCount = props.establishmentData.dailyMealCount
  form.yearlyMealCount = props.establishmentData.yearlyMealCount
  form.centralProducerSiret = props.establishmentData.centralProducerSiret
}

/* Form */
const isSaving = ref(false)
const forceRerender = ref(0)

const sendForm = (action) => {
  emit("sendForm", { form: form, action: action })
}

const getErrorMessage = (fieldName) => {
  if (props.errors.length === 0) return null
  const errorIndex = props.errors.findIndex((error) => error.field === fieldName)
  if (errorIndex === -1) return null
  const messages = props.errors[errorIndex].message
  return messages.length > 0 ? messages.join(". ") : messages[0]
}

/* Form fields initialisation */
if (props.establishmentData) {
  prefillFields()
} else resetFields()
</script>

<template>
  <section class="fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center">
    <form class="fr-col-12 fr-col-lg-7 fr-background-default--grey fr-p-2w fr-p-md-7w" @submit.prevent="">
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-2w">1. Informations générales</legend>
        <DsfrInputGroup
          v-model="form.name"
          label="Nom du groupe *"
          :label-visible="true"
          :error-message="getErrorMessage('name')"
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion *"
          v-model="form.managementType"
          :options="options.managementType"
          :error-message="getErrorMessage('managementType')"
        />
        <DsfrInputGroup
          v-model="form.centralProducerSiret"
          label="SIRET de la cuisine centrale"
          hint="Optionnel"
          :label-visible="true"
          :error-message="getErrorMessage('centralProducerSiret')"
        />
        <CanteenEstablishmentSearch
          :key="forceRerender"
          @select="(canteenInfos) => selectEstablishment(canteenInfos)"
          :error-required="getErrorMessage('sirenUniteLegale')"
          :establishment-data="prefillEstablishment"
          :has-siret="false"
          title="Mon établissement"
          class="fr-mb-4w"
          type="group"
        />
      </fieldset>
      <fieldset class="fr-mb-4w">
        <legend class="fr-h5 fr-mb-1w">2. Nombre de repas</legend>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12">
            <p class="fr-mb-0 fr-hint-text">Pour bien calculer son nombre de couverts retrouvez <a :href="documentation.calculerNombreCouverts" target="_blank">notre documentation</a></p>
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.dailyMealCount"
              label="Nombre de repas par jour *"
              :label-visible="true"
              type="number"
              :error-message="getErrorMessage('dailyMealCount')"
              />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.yearlyMealCount"
              label="Nombre de repas par an *"
              :label-visible="true"
              type="number"
              :error-message="getErrorMessage('yearlyMealCount')"
              />
          </div>
        </div>
      </fieldset>
      <div class="fr-grid-row fr-grid-row--right fr-grid-row--top">
        <DsfrButton
          v-if="showCancelButton"
          :disabled="isSaving"
          label="Annuler"
          secondary
          class="fr-mb-1v fr-mr-1v"
          @click="emit('cancel')"
        />
        <DsfrButton
          v-else
          label="Enregistrer et créer un nouveau groupe"
          :disabled="isSaving"
          secondary
          class="fr-mb-1v fr-mr-1v"
          @click="sendForm('stay-on-creation-page')"
        />
        <DsfrButton
          label="Enregistrer"
          :disabled="isSaving"
          icon="fr-icon-save-line"
          @click="sendForm('go-to-canteen-page')"
        />
      </div>
    </form>
  </section>
</template>
