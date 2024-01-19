<template>
  <DsfrCallout v-if="errorMessages.length > 1" color="red lighten-1">
    <p class="ma-0">Merci de vérifier les erreurs ci dessous :</p>
    <ul>
      <li v-for="message in errorMessages" :key="message">{{ message }}</li>
    </ul>
  </DsfrCallout>
  <DsfrCallout v-else color="red lighten-1">
    <p class="ma-0">{{ errorMessages[0] }}</p>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "./DsfrCallout"

export default {
  name: "FormErrorCallout",
  props: {
    // errorMessages is an array of Strings
    errorMessages: {
      type: Array,
      required: true,
    },
  },
  components: { DsfrCallout },
}
</script>
