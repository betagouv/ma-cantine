<script setup>
import { reactive, ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { helpers } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import achats from "@/data/achats.json"
import purchases from "@/services/purchases.js"

/* Props and emits */
const props = defineProps(["purchaseData", "showCancelButton", "showDeleteButton"])
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
  formatError: null,
  prixHt: null,
  date: null,
  familleProduits: null,
  categoriesEgalim: [],
  origine: null,
  estCircuitCourt: null,
  estLocal: null,
  definitionLocal: "",
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
}

if (props.purchaseData) prefillFields()

const showLocalDefinition = computed(() => form.estLocal)

const { required, minValue, requiredIf } = useValidators()
const rules = {
  description: { required },
  fournisseur: { required },
  prixHt: { required, minValue: minValue(0.01) },
  date: {
    required,
    maxDate: helpers.withMessage(
      "La date d'achat ne peut pas être dans le futur",
      (date) => new Date(date) < new Date()
    )
  },
  familleProduits: { required },
  definitionLocal: { required: requiredIf(showLocalDefinition) },
}

const v$ = useVuelidate(rules, form)

/* Local change */
const onLocalChange = () => {
  form.definitionLocal = ""
}

/* Form submission */
const isSaving = ref(false)

const validateForm = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return
  isSaving.value = true
  emit("sendForm", form)
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
          :error-message="formatError(v$.description)"
        />
        <datalist id="descriptions">
          <option v-for="description in autocompleteOptions.descriptions" :key="description" :value="description"></option>
        </datalist>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrInputGroup
          v-model.number="form.prixHt"
          type="number"
          label="Prix HT (€) *"
          label-visible
          :error-message="formatError(v$.prixHt)"
        />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-8">
        <DsfrInputGroup
          v-model="form.fournisseur"
          label="Fournisseur *"
          label-visible
          list="providers"
          :error-message="formatError(v$.fournisseur)"
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
          :max="today"
          :error-message="formatError(v$.date)"
        />
      </div>
    </div>

    <DsfrRadioButtonSet
      class="purchase-form__inline-col"
      v-model="form.familleProduits"
      legend="Famille de produit *"
      inline
      :options="familleProduitOptions"
      :error-message="formatError(v$.familleProduits)"
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
        />
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrCheckboxSet
          v-model="form.estCircuitCourt"
          legend="Circuit court"
          :options="estCircuitCourtOptions"
          small
          inline
        />
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <DsfrCheckboxSet
          v-model="form.estLocal"
          legend="« Local »"
          :options="estLocalOptions"
          small
          inline
          class="fr-mb-n2w"
          @change="onLocalChange"
        />
        <DsfrSelect
          v-if="showLocalDefinition"
          v-model="form.definitionLocal"
          label="Précisions *"
          hint="Précisez la provenance du produit"
          labelVisible
          :options="definitionLocalOptions"
          :error-message="formatError(v$.definitionLocal)"
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
