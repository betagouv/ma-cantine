<template>
  <div>
    <label :for="inputId" :class="labelClasses" v-if="$attrs.label">
      {{ $attrs.label }}
    </label>
    <v-textarea
      dense
      ref="textarea"
      solo
      flat
      v-bind="$attrs"
      v-on="$listeners"
      persistent-placeholder
      @input="(v) => $emit('input', v)"
    >
      <template v-slot:label><span></span></template>
    </v-textarea>
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
  data() {
    return { inputId: null }
  },
  computed: {
    value() {
      return this.$refs["textarea"].value
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["textarea"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    validate() {
      return this.$refs["textarea"].validate()
    },
    assignInputId() {
      this.inputId = this.$refs?.["textarea"]?.$el.querySelector("input")?.id
    },
  },
  mounted() {
    this.removeInnerLabel()
    this.assignInputId()
  },
}
</script>

<style scoped>
.v-textarea >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  transition: none;
}

.v-textarea.error--text >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #ff5252;
}

.v-textarea >>> .v-input__slot:focus-within {
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
