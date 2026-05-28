<script setup>
import { reactive, ref, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError, toBase64 } from "@/utils.js"

/* Props and emits */
defineProps(["showCreateButton", "showCancelButton"])
const emit = defineEmits(["sendForm", "cancel"])

/* Form fields */
const today = computed(() => new Date().toISOString().split("T")[0])

const form = reactive({
  description: null,
  provider: null,
  priceHt: null,
  date: null,
})

const { required, decimal, minValue } = useValidators()
const rules = {
  description: { required },
  provider: { required },
  priceHt: { required, decimal, minValue: minValue(0.01) },
  date: { required },
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
  <form class="purchase-form fr-mt-4w" @submit.prevent="">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-8">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.description"
              label="Description du produit *"
              label-visible
              placeholder="Yaourts bio, légumes bio de juin..."
              :error-message="formatError(v$.description)"
            />
          </div>
          <div class="fr-col-12 fr-col-md-6">
            <DsfrInputGroup
              v-model="form.provider"
              label="Fournisseur *"
              label-visible
              :error-message="formatError(v$.provider)"
            />
          </div>
        </div>

        <div class="fr-grid-row fr-grid-row--gutters">
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
      </div>

      <div class="fr-col-12 fr-col-md-4">
        <div class="purchase-form__facture fr-card ma-cantine--flex-center">
          <DsfrFileUpload
            v-model="invoiceFileInputValue"
            label="Facture"
            hint="PDF ou image (JPEG, PNG) — 10 Mo maximum"
            accept="image/jpeg,image/png,application/pdf"
            :error="invoiceFileError"
            @change="onInvoiceFileChange"
          />
        </div>
      </div>
    </div>

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
        v-if="showCancelButton"
        :disabled="isSaving"
        label="Annuler"
        secondary
        class="fr-mr-1w"
        @click="emit('cancel')"
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
