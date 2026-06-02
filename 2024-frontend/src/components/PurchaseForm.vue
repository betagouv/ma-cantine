<script setup>
import { reactive, ref, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError, toBase64 } from "@/utils.js"
import achats from "@/data/achats.json"

/* Props and emits */
defineProps(["showCreateButton"])
const emit = defineEmits(["sendForm"])

/* Form fields */
const today = computed(() => new Date().toISOString().split("T")[0])

const form = reactive({
  description: null,
  provider: null,
  priceHt: null,
  date: null,
  family: null,
  characteristics: [],
  characteristicsEgalim: [],
  characteristicsOrigines: [],
  characteristicsCircuitCourt: [],
  characteristicsLocal: [],
  localDefinition: null,
})

const familleProduitOptions = Object.values(achats.familleProduit)
const categoriesEgalimOptions = Object.values(achats.categoriesEgalim)
const categoriesOriginesOptions = Object.values(achats.categoriesOrigines)
const estCircuitCourtOptions = Object.values(achats.estCircuitCourt)
const estLocalOptions = Object.values(achats.estLocal)
const definitionLocalOptions = Object.values(achats.definitionLocal).map(option => ({ value: option.value, text: option.label }))

const showLocalDefinition = computed(() => form.characteristicsLocal.length > 0)

const { required, decimal, minValue, requiredIf } = useValidators()
const rules = {
  description: { required },
  provider: { required },
  priceHt: { required, decimal, minValue: minValue(0.01) },
  date: { required },
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

  const payload = { ...form }
  if (invoiceFile.value) payload.invoiceFile = await toBase64(invoiceFile.value)
  emit("sendForm", { form: payload, action })
}
</script>

<template>
  <form class="purchase-form fr-p-2w fr-p-md-7w fr-col-12 fr-col-lg-7 fr-background-default--grey fr-mt-4w" @submit.prevent="">
    <DsfrInputGroup
      v-model="form.description"
      label="Description du produit *"
      label-visible
      placeholder="Yaourts bio, légumes bio de juin..."
      :error-message="formatError(v$.description)"
    />
    <DsfrInputGroup
      v-model="form.provider"
      label="Fournisseur *"
      label-visible
      :error-message="formatError(v$.provider)"
    />
    <DsfrInputGroup
      v-model.number="form.priceHt"
      type="number"
      label="Prix HT (€) *"
      label-visible
      :error-message="formatError(v$.priceHt)"
    />
    <DsfrInputGroup
      v-model="form.date"
      type="date"
      label="Date d'achat *"
      label-visible
      :max="today"
      :error-message="formatError(v$.date)"
    />
    <DsfrFileUpload
      v-model="invoiceFileInputValue"
      label="Facture"
      hint="PDF ou image (JPEG, PNG) — 10 Mo maximum"
      accept="image/jpeg,image/png,application/pdf"
      :error="invoiceFileError"
      class="fr-mb-3w"
      @change="onInvoiceFileChange"
    />
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

    <div class="fr-grid-row fr-grid-row--right fr-grid-row--gutters fr-mt-4w">
      <DsfrButton
        v-if="showCreateButton"
        :disabled="isSaving"
        label="Enregistrer et ajouter un nouvel achat"
        secondary
        class="fr-mr-1w"
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
