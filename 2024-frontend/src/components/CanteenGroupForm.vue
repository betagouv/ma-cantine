<script setup>
import { ref, computed, reactive } from "vue"
import { helpers } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import options from "@/constants/canteen-establishment-form-options"
import CanteenEstablishmentSearch from "@/components/CanteenEstablishmentSearch.vue"

/* Data */
const props = defineProps(["establishmentData", "showCancelButton"])
const emit = defineEmits(["sendForm", "cancel"])
const prefillEstablishment = ref(props.establishmentData)

/* SIREN */
const selectEstablishment = (canteenInfos) => {
  form.sirenUniteLegale = canteenInfos.siren?.replace(" ", "")
}

/* FORM */
const form = reactive({})

const resetFields = () => {
  form.hasSiret = "no-siret"
  form.siret = null
  form.sirenUniteLegale = null
  form.name = null
  form.managementType = null
  form.dailyMealCount = null
  form.yearlyMealCount = null
  form.centralProducerSiret = null
}

const prefillFields = () => {
  form.hasSiret = "no-siret"
  form.sirenUniteLegale = props.establishmentData.sirenUniteLegale
  form.name = props.establishmentData.name
  form.managementType = props.establishmentData.managementType
  form.dailyMealCount = props.establishmentData.dailyMealCount
  form.yearlyMealCount = props.establishmentData.yearlyMealCount
  form.centralProducerSiret = props.establishmentData.centralProducerSiret
}

/* Fields verification */
const { required, integer, minValue, maxValue, minLength, maxLength } = useValidators()
const yearlyMealMinValue = computed(() => Math.max(form.dailyMealCount, 420))
const dailyMealMaxValue = computed(() => form.yearlyMealCount)

const rules = {
  name: { required },
  sirenUniteLegale: { required },
  managementType: { required },
  centralProducerSiret: {
    minLength: helpers.withMessage("Le SIRET doit contenir 14 caractères", minLength(14)),
    maxLength: helpers.withMessage("Le SIRET doit contenir 14 caractères", maxLength(14)),
  },
  dailyMealCount: { required, integer, minValue: minValue(3), maxValue: maxValue(dailyMealMaxValue) },
  yearlyMealCount: { required, integer, minValue: minValue(yearlyMealMinValue) },
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
      <fieldset class="fr-mb-4w">
        <DsfrInputGroup
          v-model="form.name"
          label="Nom du groupe *"
          :error-message="formatError(v$.name)"
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion *"
          v-model="form.managementType"
          :options="options.managementType"
          :error-message="formatError(v$.managementType)"
        />
        <DsfrInputGroup
          v-model="form.centralProducerSiret"
          label="SIRET du livreur"
          hint="Optionnel"
          :label-visible="true"
          :error-message="formatError(v$.centralProducerSiret)"
        />
        <CanteenEstablishmentSearch
          :key="forceRerender"
          @select="(canteenInfos) => selectEstablishment(canteenInfos)"
          :error-required="formatError(v$.sirenUniteLegale)"
          :establishment-data="prefillEstablishment"
          :has-siret="false"
          title="Mon établissement"
          class="fr-mb-4w"
        />
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.dailyMealCount"
              label="Nombre de repas par jour *"
              :label-visible="true"
              type="number"
              :error-message="formatError(v$.dailyMealCount)"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.yearlyMealCount"
              label="Nombre de repas par an *"
              :label-visible="true"
              type="number"
              :error-message="formatError(v$.yearlyMealCount)"
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
          @click="validateForm('stay-on-creation-page')"
        />
        <DsfrButton
          label="Enregistrer"
          :disabled="isSaving"
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
