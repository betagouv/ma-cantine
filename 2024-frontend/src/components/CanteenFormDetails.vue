<script setup>
import { inject, ref } from "vue"
import { formatError } from "@/utils.js"
const { updateForm, v$ } = inject("form")
const name = ref()
</script>

<template>
  <fieldset class="fr-mb-4w">
    <legend class="fr-h5 fr-mb-2w">2. Coordonnées</legend>
    <DsfrInputGroup
      v-model="name"
      label="Nom de la cantine *"
      hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
      :label-visible="true"
      :error-message="formatError(v$.name)"
      @update:modelValue="updateForm({ name })"
    />
  </fieldset>
</template>
