<script setup>
import { reactive, ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { helpers } from "@vuelidate/validators"
import { formatError, toBase64 } from "@/utils.js"
import achats from "@/data/achats.json"
import purchases from "@/services/purchases.js"

/* Props and emits */
const props = defineProps(["purchaseData", "showCreateButton", "showCancelButton", "showDeleteButton"])
const emit = defineEmits(["sendForm", "cancel", "delete"])

/* Form fields */
const today = computed(() => new Date().toISOString().split("T")[0])
const autocompleteOptions = computedAsync(async () => {
  const response = await purchases.fetchPurchasesOptions()
  return {
    descriptions: response.products || [],
    providers: response.providers || [],
  }
}, {})

const form = reactive({
  description: null,
  provider: null,
  priceHt: null,
  date: null,
  family: null,
  characteristicsEgalim: [],
  characteristicsOrigines: [],
  characteristicsCircuitCourt: [],
  characteristicsLocal: [],
  localDefinition: "",
})

const familleProduitOptions = Object.values(achats.familleProduit)
const categoriesEgalimOptions = Object.values(achats.categoriesEgalim)
const categoriesOriginesOptions = Object.values(achats.categoriesOrigines)
const estCircuitCourtOptions = Object.values(achats.estCircuitCourt)
const estLocalOptions = Object.values(achats.estLocal)
const definitionLocalOptions = Object.values(achats.definitionLocal).map(option => ({ value: option.value, text: option.label }))

const egalimValues = categoriesEgalimOptions.map((option) => option.value)
const originesValues = categoriesOriginesOptions.map((option) => option.value)
const circuitCourtValues = estCircuitCourtOptions.map((option) => option.value)
const localValues = estLocalOptions.map((option) => option.value)

const prefillFields = () => {
  form.description = props.purchaseData.description
  form.provider = props.purchaseData.provider
  const hasPriceHt = props.purchaseData.priceHt !== null && props.purchaseData.priceHt !== undefined
  form.priceHt = hasPriceHt ? Number(props.purchaseData.priceHt) : null
  form.date = props.purchaseData.date
  form.family = props.purchaseData.family
  form.localDefinition = props.purchaseData.localDefinition || ""
  const characteristics = props.purchaseData.characteristics || []
  form.characteristicsEgalim = characteristics.filter((c) => egalimValues.includes(c))
  form.characteristicsOrigines = characteristics.filter((c) => originesValues.includes(c))
  form.characteristicsCircuitCourt = characteristics.filter((c) => circuitCourtValues.includes(c))
  form.characteristicsLocal = characteristics.filter((c) => localValues.includes(c))
  form.invoiceUrl = props.purchaseData.invoiceFile
}

if (props.purchaseData) prefillFields()

const showLocalDefinition = computed(() => form.characteristicsLocal.length > 0)

const { required, decimal, minValue, requiredIf } = useValidators()
const rules = {
  description: { required },
  provider: { required },
  priceHt: { required, decimal, minValue: minValue(0.01) },
  date: {
    required,
    maxDate: helpers.withMessage(
      "La date d'achat ne peut pas être dans le futur",
      (date) => new Date(date) < new Date()
    )
  },
  family: { required },
  localDefinition: { required: requiredIf(showLocalDefinition) },
}

const v$ = useVuelidate(rules, form)

/* Invoice file (Base64FileField on the backend; size enforced client-side) */
const invoiceMaxSize = 10 * 1024 * 1024 // 10 Mo
const invoiceFile = ref(null)
const invoiceFileInputValue = ref("")
const invoiceFileError = ref("")

const onInvoiceFileChange = (files) => {
  invoiceFileError.value = ""
  const file = files?.[0]
  if (!file) {
    invoiceFile.value = null
    return
  }
  if (file.size > invoiceMaxSize) {
    invoiceFileError.value = "Le fichier dépasse la taille maximale de 10 Mo."
    invoiceFile.value = null
    return
  }
  invoiceFile.value = file
}

/* Form submission */
const isSaving = ref(false)

const validateForm = async (action) => {
  const isValid = await v$.value.$validate()
  if (!isValid || invoiceFileError.value) return
  isSaving.value = true
  const payload = formatPayload(form)
  if (invoiceFile.value) payload.invoiceFile = await toBase64(invoiceFile.value)
  emit("sendForm", { form: payload, action })
}

const formatPayload = (form) => {
  const payload = { ...form }
  payload.characteristics = [...payload.characteristicsEgalim, ...payload.characteristicsOrigines, ...payload.characteristicsCircuitCourt, ...payload.characteristicsLocal]
  delete payload.characteristicsEgalim
  delete payload.characteristicsOrigines
  delete payload.characteristicsCircuitCourt
  delete payload.characteristicsLocal
  return payload
}
</script>

<template>
  <form class="purchase-form fr-p-2w fr-p-md-7w fr-col-12 fr-col-lg-7 fr-background-default--grey fr-mt-4w" @submit.prevent="">
    <DsfrInputGroup
      v-model="form.description"
      label="Description du produit *"
      label-visible
      list="descriptions"
      placeholder="Yaourts bio, légumes bio de juin..."
      :error-message="formatError(v$.description)"
    />
    <datalist id="descriptions">
      <option v-for="description in autocompleteOptions.descriptions" :key="description" :value="description"></option>
    </datalist>
    <DsfrInputGroup
      v-model="form.provider"
      label="Fournisseur *"
      label-visible
      list="providers"
      :error-message="formatError(v$.provider)"
    />
    <datalist id="providers">
      <option v-for="provider in autocompleteOptions.providers" :key="provider" :value="provider"></option>
    </datalist>
    <div class="fr-grid-row fr-grid-row--gutters fr-mb-2w">
      <div class="fr-col-12 fr-col-md-6">
        <DsfrInputGroup
          v-model.number="form.priceHt"
          type="number"
          label="Prix HT (€) *"
          label-visible
          :error-message="formatError(v$.priceHt)"
        />
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <DsfrInputGroup
          v-model="form.date"
          type="date"
          label="Date d'achat *"
          label-visible
          :max="today"
          :error-message="formatError(v$.date)"
        />
      </div>
    </div>
    <div class="fr-mb-3w">
      <p class="fr-legend-text fr-mb-1w">Facture</p>
      <div class="fr-grid-row fr-grid-row--top fr-grid-row--gutters">
        <div v-if="form.invoiceUrl" class="fr-col-12 fr-col-md-6">
          <p class="fr-mb-2w">Vous avez déjà importé une facture pour cet achat, accéder au fichier en <a :href="form.invoiceUrl" target="_blank">cliquant ici</a>.</p>
        </div>
        <div class="fr-col-12" :class="{ 'fr-col-md-6': form.invoiceUrl }">
          <DsfrFileUpload
            v-model="invoiceFileInputValue"
            :label="form.invoiceUrl ? 'Télécharger un nouveau fichier' : 'Télécharger un fichier'"
            hint="PDF ou image (JPEG, PNG) — 10 Mo maximum"
            accept="image/jpeg,image/png,application/pdf"
            :error="invoiceFileError"
            @change="onInvoiceFileChange"
          />
        </div>
      </div>
    </div>
    <DsfrRadioButtonSet
      v-model="form.family"
      legend="Famille de produit *"
      :options="familleProduitOptions"
      :error-message="formatError(v$.family)"
    />

    <DsfrMultiselect
      v-model="form.characteristicsEgalim"
      label="Catégories EGalim"
      labelVisible
      :options="categoriesEgalimOptions"
      id-key="value"
      :filtering-keys="['label', 'hint']"
      search
      maxOverflowHeight="300px"
    >
      <template #checkbox-label="{ option }">
        <div>
          <p class="fr-mb-0">{{ option.label }}</p>
          <p v-if="option.hint" class="fr-mb-0 fr-hint-text">{{ option.hint }}</p>
        </div>
      </template>
    </DsfrMultiselect>

    <DsfrCheckboxSet
      v-model="form.characteristicsOrigines"
      legend="Origine"
      :options="categoriesOriginesOptions"
      small
      inline
    />

    <DsfrCheckboxSet
      v-model="form.characteristicsCircuitCourt"
      legend="Circuit court"
      :options="estCircuitCourtOptions"
      small
      inline
    />

    <DsfrCheckboxSet
      v-model="form.characteristicsLocal"
      legend="« Local »"
      :options="estLocalOptions"
      small
      inline
      class="fr-mb-n2w"
    />
    <DsfrSelect
      v-if="showLocalDefinition"
      v-model="form.localDefinition"
      label="Précisions *"
      hint="Précisez la provenance du produit"
      labelVisible
      :options="definitionLocalOptions"
      :error-message="formatError(v$.localDefinition)"
    />
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
        v-if="showCreateButton"
        :disabled="isSaving"
        label="Enregistrer et ajouter un nouvel achat"
        secondary
        @click="validateForm('stay-on-creation-page')"
      />
      <DsfrButton
        :disabled="isSaving"
        label="Enregistrer"
        icon="fr-icon-save-line"
        @click="validateForm('go-to-purchases-list')"
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
}
</style>
