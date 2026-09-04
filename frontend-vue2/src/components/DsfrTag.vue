<template>
  <v-chip
    v-if="clickable"
    :close="closeable"
    @click="clickAction"
    @click:close="closeAction"
    class="ma-1"
    :color="tagColor"
    close-label="Fermer"
    close-icon="$close-line"
    :small="small"
    :aria-pressed="clickable ? selected.toString() : ''"
    :tag="clickable ? 'button' : 'span'"
  >
    {{ text }}
  </v-chip>
  <span v-else class="tag fr-text-xs ma-1">
    <v-icon v-if="icon" x-small>{{ icon }}</v-icon>
    {{ text }}
  </span>
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
    clickable: {
      type: Boolean,
      default: true,
    },
    icon: {
      type: String,
      required: false,
    },
    selected: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    tagColor() {
      if (this.color) return this.color
      else if (this.closeable || this.selected) return "primary"
      else if (this.clickable) return "primary lighten-5 primary--text"
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
<style scoped>
.tag {
  display: inline-flex;
  padding: 2px 8px;
  justify-content: center;
  align-items: center;
  gap: 2px;
  border-radius: 12px;
  background-color: #eee;
  color: #161616;
  width: fit-content;
}
.tag .v-icon {
  color: #161616;
}
.tag.top-left {
  position: absolute;
  left: 12px;
  top: 12px;
}
</style>
