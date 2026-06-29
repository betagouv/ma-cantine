<script setup>
import { reactive, ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import achats from "@/data/achats.json"
import purchases from "@/services/purchases.js"

/* Props and emits */
const props = defineProps(["purchaseData", "showCancelButton", "showDeleteButton", "errors"])
const emit = defineEmits(["sendForm", "cancel", "delete"])

/* Form fields */
const autocompleteOptions = computedAsync(async () => {
  const response = await purchases.fetchPurchasesOptions()
  return {
    descriptions: response.products || [],
    providers: response.providers || [],
  }
}, {})

const form = reactive({
  description: null,
  fournisseur: null,
  prixHt: null,
  date: null,
  familleProduits: null,
  categoriesEgalim: [],
  origine: null,
  estCircuitCourt: false,
  estLocal: false,
  definitionLocal: "",
  definitionLocalKm: null,
})

const familleProduitOptions = Object.values(achats.familleProduit)
const categoriesEgalimOptions = Object.values(achats.categoriesEgalim)
const categoriesOriginesOptions = Object.values(achats.categoriesOrigines).map(option => ({ value: option.value, text: option.label }))
const estCircuitCourtOptions = Object.values(achats.estCircuitCourt)
const estLocalOptions = Object.values(achats.estLocal)
const definitionLocalOptions = Object.values(achats.definitionLocal).map(option => ({ value: option.value, text: option.label }))

const prefillFields = () => {
  form.description = props.purchaseData.description
  form.fournisseur = props.purchaseData.fournisseur
  form.prixHt = props.purchaseData.prixHt
  form.date = props.purchaseData.date
  form.familleProduits = props.purchaseData.familleProduits
  form.categoriesEgalim = props.purchaseData.categoriesEgalim
  form.origine = props.purchaseData.origine
  form.estCircuitCourt = props.purchaseData.estCircuitCourt
  form.estLocal = props.purchaseData.estLocal
  form.definitionLocal = props.purchaseData.definitionLocal
  form.definitionLocalKm = props.purchaseData.definitionLocalKm
}

if (props.purchaseData) prefillFields()

/* Fields errors */
const showLocalDefinition = computed(() => form.estLocal)
const showKMDefinition = computed(() => form.estLocal && form.definitionLocal === 'KM')

const { required } = useValidators()
const rules = {
  description: { required },
  prixHt: { required },
  date: { required },
  familleProduits: { required },
}

const v$ = useVuelidate(rules, form)

const backendErrors = computed(() => {
  if (!props.errors) return {}
  const fieldsName = Object.keys(form)
  const valuesErrors = Object.values(props.errors)
  const errors = Object.fromEntries(fieldsName.map(field => [field, false]))

  for (const error of valuesErrors) {
    if (fieldsName.includes(error.field)) {
      errors[error.field] = error.message.join(". ")
    }
  }
  return errors
})

/* Local change */
const onLocalChange = () => {
  form.definitionLocal = ""
}

const onDefinitionLocalChange = () => {
  form.definitionLocalKm = null
}

/* Form submission */
const isSaving = ref(false)

const validateForm = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return
  isSaving.value = true
  const payload = formatPayload(form)
  emit("sendForm", payload)
  isSaving.value = false
}

const formatPayload = (form) => {
  const payload = { ...form }
  // Field origine cannot be empty
  if (payload.origine === '' || payload.origine === null) delete payload.origine
  // Field prixHt must use "." decimal separator and not ","
  const priceDot = typeof payload.prixHt === 'string' ? payload.prixHt.replace(',', '.') : payload.prixHt
  payload.prixHt = priceDot
  return payload
}
</script>

<template>
  <form class="purchase-form" @submit.prevent="">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-8">
        <DsfrInputGroup
          v-model="form.description"
          label="Description du produit *"
          label-visible
          list="descriptions"
          placeholder="Yaourts bio, légumes bio de juin..."
          :error-message="formatError(v$.description) || backendErrors.description"
        />
        <datalist id="descriptions">
          <option v-for="description in autocompleteOptions.descriptions" :key="description" :value="description"></option>
        </datalist>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrInputGroup
          v-model="form.prixHt"
          label="Prix HT (€) *"
          label-visible
          :error-message="formatError(v$.prixHt) || backendErrors.prixHt"
          class="fr-mb-4w"
        />
      </div>
    </div>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-8">
        <DsfrInputGroup
          v-model="form.fournisseur"
          label="Fournisseur"
          label-visible
          list="providers"
          :error-message="backendErrors.fournisseur"
        />
        <datalist id="providers">
          <option v-for="provider in autocompleteOptions.providers" :key="provider" :value="provider"></option>
        </datalist>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrInputGroup
          v-model="form.date"
          type="date"
          label="Date d'achat *"
          label-visible
          :error-message="formatError(v$.date) || backendErrors.date"
          class="fr-mb-4w"
        />
      </div>
    </div>

    <DsfrRadioButtonSet
      class="purchase-form__inline-col"
      v-model="form.familleProduits"
      legend="Famille de produit *"
      inline
      :options="familleProduitOptions"
      :error-message="formatError(v$.familleProduits) || backendErrors.familleProduits"
    />

    <DsfrCheckboxSet
      class="purchase-form__inline-col"
      v-model="form.categoriesEgalim"
      legend="Catégories EGalim"
      :options="categoriesEgalimOptions"
      small
      inline
    />

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-4">
        <DsfrSelect
          v-model="form.origine"
          label="Origine"
          :options="[{ value: '', text: '--' }, ...categoriesOriginesOptions]"
          :error-message="backendErrors.origine"
          class="fr-mb-4w"
        />
      </div>
    </div>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-12">
        <DsfrCheckboxSet
          v-model="form.estCircuitCourt"
          legend="Circuit court"
          :options="estCircuitCourtOptions"
          :error-message="backendErrors.estCircuitCourt"
          small
          inline
        />
      </div>
    </div>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-4">
        <DsfrCheckboxSet
          v-model="form.estLocal"
          legend="« Local »"
          :options="estLocalOptions"
          :error-message="backendErrors.estLocal"
          small
          inline
          @change="onLocalChange"
        />
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrSelect
          v-if="showLocalDefinition"
          v-model="form.definitionLocal"
          label="Précisez la provenance du produit"
          labelVisible
          :options="[{ value: '', text: '--' }, ...definitionLocalOptions]"
          :error-message="backendErrors.definitionLocal"
          @change="onDefinitionLocalChange"
        />
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrInputGroup
          v-if="showKMDefinition"
          v-model.number="form.definitionLocalKm"
          label="Distance (en km)"
          label-visible
          :error-message="backendErrors.definitionLocalKm"
        />
      </div>
    </div>

    <div class="fr-mt-6w ma-cantine--flex-end">
      <DsfrButton
        v-if="showDeleteButton"
        :disabled="isSaving"
        label="Supprimer"
        icon="fr-icon-delete-bin-line"
        tertiary
        @click="emit('delete')"
      />
      <DsfrButton
        v-if="showCancelButton"
        :disabled="isSaving"
        label="Annuler"
        secondary
        @click="emit('cancel')"
      />
      <DsfrButton
        :disabled="isSaving"
        label="Enregistrer"
        icon="fr-icon-save-line"
        @click="validateForm()"
      />
    </div>
  </form>
</template>

<style lang="scss">
.purchase-form {
  &__facture {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  &__inline-col {
    .fr-fieldset {
      align-items: flex-start !important;
    }
    .fr-fieldset__element--inline {
      width: 33% !important;
    }
  }
}
</style>
