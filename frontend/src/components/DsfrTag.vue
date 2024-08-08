<template>
  <v-chip
    :close="closeable"
    @click="clickAction"
    @click:close="closeAction"
    class="ma-1"
    :color="tagColor"
    close-label="Fermer"
    close-icon="$close-line"
    :small="small"
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
    color: {
      type: String,
    },
    small: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    tagColor() {
      if (this.color) return this.color
      else if (this.closeable) return "primary"
      return "grey lighten-4"
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
