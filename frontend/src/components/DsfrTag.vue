<template>
  <v-chip
    :close="closeable"
    @click="clickAction"
    @click:close="closeAction"
    class="ma-1"
    color="primary"
    close-label="Fermer"
    close-icon="$close-line"
  >
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
    closeable: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    clickAction() {
      this.$emit(this.closeable ? "close" : "click")
    },
    closeAction() {
      if (this.closeable) this.$emit("close")
    },
  },
}
</script>
