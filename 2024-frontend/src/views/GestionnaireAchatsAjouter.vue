<script setup>
import { reactive, ref, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { useRootStore } from "@/stores/root"
import { formatError } from "@/utils.js"
import urlService from "@/services/urls.js"
import purchasesService from "@/services/purchases.js"

/* Router and store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Canteen */
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)

/* Form */
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

/* Submit */
const isSaving = ref(false)

const resetForm = () => {
  form.description = null
  form.provider = null
  form.priceHt = null
  form.date = null
  v$.value.$reset()
  window.scrollTo(0, 0)
}

const savePurchase = async (stayOnPage = false) => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  isSaving.value = true
  const payload = { ...form, canteen: canteenId }
  const response = await purchasesService.createPurchase(payload)
  isSaving.value = false

  if (!response?.id) {
    store.notifyServerError(response)
    return
  }

  store.notify({
    title: "Achat enregistré",
    message: `L'achat « ${form.description} » a bien été enregistré pour la cantine « ${canteenName} ».`,
    status: "success",
  })

  if (stayOnPage) resetForm()
  else router.push({ name: "PurchasesHome" })
}
</script>

<template>
  <h1>{{ route.meta.title }}</h1>

  <form class="fr-mt-4w" @submit.prevent="">
    <DsfrInputGroup
      v-model="form.description"
      label="Description du produit *"
      label-visible
      hint="Ex : Yaourts bio, légumes bio de juin..."
      :error-message="formatError(v$.description)"
    />
    <DsfrInputGroup
      v-model="form.provider"
      label="Fournisseur *"
      label-visible
      :error-message="formatError(v$.provider)"
    />
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

    <div class="fr-grid-row fr-grid-row--right fr-grid-row--gutters fr-mt-4w">
      <DsfrButton
        label="Enregistrer et ajouter un nouvel achat"
        secondary
        class="fr-mr-1w"
        @click="savePurchase(true)"
      />
      <DsfrButton
        label="Enregistrer"
        icon="fr-icon-save-line"
        @click="savePurchase(false)"
      />
    </div>
  </form>
</template>
