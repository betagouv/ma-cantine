<script setup>
import "@/css/dsfr-multi-select.css"
import { ref, reactive, computed } from "vue"
import sectorsService from "@/services/sectors"
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

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.name = ""
  form.economicModel = ""
  form.managementType = ""
  form.productionType = ""
  form.sectorCategory = ""
  form.sectorActivity = []
  form.ministry = ""
}
initFields()

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
  for (let i = 0; i < form.sectorActivity.length; i++) {
    const key = form.sectorActivity[i]
    const activity = sectorsActivityOptions.value[key]
    const hasLineMinistry = activity.hasLineMinistry
    if (!hasLineMinistry) continue
    showMinistrySelector.value = true
    break
  }
}
</script>

<template>
  <section class="fr-p-3w fr-background-alt--blue-france fr-mt-4w fr-grid-row fr-grid-row--center">
    <form class="fr-col-7 fr-background-default--grey fr-p-2w fr-p-md-7w">
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">1. SIRET</legend>
      </fieldset>
      <fieldset class="fr-mb-7w">
        <legend class="fr-h5">2. Coordonnées</legend>
        <DsfrInput
          v-model="form.name"
          label="Nom de la cantine"
          :label-visible="true"
          hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
        />
      </fieldset>
      <fieldset class="fr-mb-3w">
        <legend class="fr-h5">3. Caractéristiques</legend>
        <DsfrRadioButtonSet
          legend="Type d’établissement"
          v-model="form.economicModel"
          :small="true"
          :options="options.economicModel"
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion"
          v-model="form.managementType"
          :small="true"
          :options="options.managementType"
        />
        <DsfrRadioButtonSet
          legend="Mode de production"
          v-model="form.productionType"
          :small="true"
          :options="options.productionType"
        />
      </fieldset>
      <fieldset>
        <legend class="fr-h5">4. Secteur</legend>
        <DsfrSelect
          v-model="form.sectorCategory"
          label="Catégorie de secteur"
          labelVisible
          :options="sectorsCategoryOptions"
          @change="changeCategory()"
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
        >
          <template #no-results>
            Sélectionner une catégorie de secteur pour pouvoir sélectionner des secteurs d'activité
          </template>
        </DsfrMultiselect>
        <DsfrSelect
          v-if="showMinistrySelector"
          v-model="form.ministry"
          label="Ministère de tutelle"
          labelVisible
          :options="ministryOptions"
        />
      </fieldset>
    </form>
  </section>
</template>
