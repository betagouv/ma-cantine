<template>
  <div>
    <label :for="inputId" :class="labelClasses" v-if="$attrs.label">
      {{ $attrs.label }}
    </label>
    <v-text-field
      density="compact"
      single-line
      ref="text-field"
      v-bind="$attrs"
      persistent-placeholder
      @update:model-value="(v) => $emit('input', v)"
    >
      <template v-slot:label><span></span></template>

      <template v-for="(_, name) in $slots" v-slot:[name]>
        <slot :name="name" />
      </template>
    </v-text-field>
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
    lazyValue() {
      return this.$refs["text-field"].lazyValue
    },
    value() {
      return this.$refs["text-field"].value
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["text-field"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    validate() {
      return this.$refs["text-field"].validate()
    },
    assignInputId() {
      this.inputId = this.$refs?.["text-field"]?.$refs?.["input"]?.id
    },
  },
  mounted() {
    this.removeInnerLabel()
    this.assignInputId()
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

.v-text-field >>> .v-input__slot:focus-within {
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
