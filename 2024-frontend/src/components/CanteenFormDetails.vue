<script setup>
import { ref } from "vue"
defineProps(["error"])
const name = ref("")
</script>

<template>
  <fieldset class="fr-mb-4w">
    <legend class="fr-h5 fr-mb-2w">2. Coordonnées</legend>
    <DsfrInputGroup
      v-model="name"
      label="Nom de la cantine *"
      hint="Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple :  École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne..."
      :label-visible="true"
      :error-message="error"
      @change="$emit('update', { name: name })"
    />
  </fieldset>
</template>
