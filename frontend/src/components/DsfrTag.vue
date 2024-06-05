<template>
  <v-chip close @click="closeAction" @click:close="closeAction" class="ma-1" color="primary" close-label="Fermer">
    {{ text }}
  </v-chip>
</template>

<script>
export default {
  name: "DsfrTag",
  props: {
    text: {
      type: String,
      required: true,
    },
    closeAction: {
      type: Function,
      required: true, // there is definitely a use case without
    },
  },
}
</script>
