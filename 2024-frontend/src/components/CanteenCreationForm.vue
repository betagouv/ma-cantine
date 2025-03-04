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
  form.dailyMealCount = ""
  form.yearlyMealCount = ""
  form.centralProducerSiret = ""
  form.satelliteCanteensCount = ""
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

/* Dynamic Inputs */
const hideDailyMealCount = computed(() => form.productionType === "central")
const showCentralProducerSiret = computed(() => form.productionType === "site_cooked_elsewhere")
const showSatelliteCanteensCount = computed(
  () => form.productionType === "central" || form.productionType === "central_serving"
)
</script>

<template>
  <section
    class="canteen-creation-form fr-background-alt--blue-france fr-p-3w fr-mt-4w fr-grid-row fr-grid-row--center"
  >
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
        <DsfrInput v-if="showCentralProducerSiret" v-model="form.centralProducerSiret" :label-visible="true">
          <template #label>
            SIRET du livreur
            <span class="fr-hint-text">
              Vous ne le connaissez pas ? Trouvez-le avec
              <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
            </span>
          </template>
        </DsfrInput>
        <DsfrInput
          v-if="showSatelliteCanteensCount"
          v-model="form.satelliteCanteensCount"
          type="number"
          label="Nombre de cuisine satellite"
          hint="Nombre de cantines/lieux de service à qui je fournis des repas"
          :label-visible="true"
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
      <fieldset>
        <legend class="fr-h5">5. Nombre de repas</legend>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-6">
            <DsfrInput
              :class="{
                hide: hideDailyMealCount,
              }"
              v-model="form.dailyMealCount"
              label="Par jour"
              :label-visible="true"
              :disabled="hideDailyMealCount"
              :hint="hideDailyMealCount ? 'Concerne uniquement les cantines recevant des convives' : ''"
              type="number"
            />
          </div>
          <div class="fr-col-6">
            <DsfrInput v-model="form.yearlyMealCount" label="Par an" :label-visible="true" type="number" />
          </div>
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
}
</style>
