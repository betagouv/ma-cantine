<template>
  <div>
    <label :for="inputId" :class="labelClasses">
      {{ $attrs.label }}
    </label>
    <v-autocomplete
      dense
      height="40"
      ref="autocomplete"
      solo
      flat
      v-bind="$attrs"
      v-on="$listeners"
      persistent-placeholder
      @input="(v) => $emit('input', v)"
    >
      <template v-slot:label><span></span></template>
    </v-autocomplete>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    labelClasses: {
      type: String,
      required: false,
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left",
    },
  },
  computed: {
    inputId() {
      return this.$refs?.["autocomplete"]?.$refs?.["input"].id
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["autocomplete"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
  },
  mounted() {
    this.removeInnerLabel()
  },
}
</script>

<style scoped>
.v-autocomplete >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  transition: none;
}

.v-autocomplete.error--text >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #ff5252;
}

.v-autocomplete >>> .v-input__slot:focus-within {
  outline-style: solid;
  outline-width: 2px;
  outline-color: #0a76f6;
  outline-offset: 2px;
  border-radius: 2px 2px 0 0;
}

div > label {
  display: block;
}
</style>
