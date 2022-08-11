<template>
  <v-text-field
    dense
    height="40"
    ref="text-field"
    solo
    flat
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
  >
    <template v-slot:label><span></span></template>
  </v-text-field>
</template>

<script>
export default {
  inheritAttrs: false,
  data() {
    return {
      inputId: null,
    }
  },
  methods: {
    removeLabels() {
      const labels = this.$refs["text-field"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    createLabel() {
      const label = document.createElement("label")
      label.setAttribute("for", this.$refs["text-field"].$refs["input"].id)
      label.classList.add("mb-2")
      label.classList.add("text-sm-subtitle-1")
      label.classList.add("text-body-2")
      label.textContent = this.$attrs.label
      this.$refs["text-field"].$el.getElementsByClassName("v-input__control")[0].prepend(label)
    },
  },
  mounted() {
    this.removeLabels()
    this.createLabel()
  },
}
</script>

<style scoped>
.v-text-field >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  transition: none;
}

.v-text-field.error--text >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #ff5252;
}

.v-text-field.v-text-field--solo.v-input--dense >>> .v-input__prepend-outer,
.v-text-field.v-text-field--solo.v-input--dense >>> .v-input__append-outer {
  margin-top: 15px !important;
}

.v-text-field >>> .v-input__slot:focus-within {
  outline-style: solid;
  outline-width: 2px;
  outline-color: #0a76f6;
  outline-offset: 2px;
  border-radius: 2px 2px 0 0;
}
</style>
