<script setup>
import { reactive } from "vue"
import options from "@/constants/canteen-creation-form-options"

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.name = ""
  form.economicModel = ""
  form.managementType = ""
  form.productionType = ""
}
initFields()
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
      <fieldset class="fr-mb-7w">
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
    </form>
  </section>
</template>
