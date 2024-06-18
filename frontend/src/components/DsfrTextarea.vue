<template>
  <div>
    <label :for="inputId" :class="labelClasses" v-if="$attrs.label">
      {{ $attrs.label }}
      <span v-if="hintText" class="fr-hint-text">{{ hintText }}</span>
      <span v-else-if="optional" class="fr-hint-text">Optionnel</span>
    </label>
    <slot name="label"></slot>
    <v-textarea
      dense
      ref="textarea"
      solo
      flat
      v-bind="$attrs"
      v-on="$listeners"
      persistent-placeholder
      @input="(v) => $emit('input', v)"
      :aria-describedby="errorMessageId"
      :aria-invalid="hasError"
    >
      <template v-slot:label><span></span></template>

      <!-- For RGAA 8.9 error messages should also be in p tags, by default in vuetify 2 they're in divs -->
      <template v-slot:message="{ key, message }">
        <p :id="errorMessageId" :key="key" class="mb-0">{{ message }}</p>
      </template>
    </v-textarea>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  inject: {
    form: { default: null },
  },
  inheritAttrs: false,
  props: {
    labelClasses: {
      type: String,
      required: false,
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left",
    },
    hintText: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      inputId: null,
      hasError: null,
    }
  },
  computed: {
    value() {
      return this.$refs["textarea"].value
    },
    reset() {
      return this.$refs["textarea"].reset
    },
    optional() {
      return !validators._includesRequiredValidator(this.$attrs.rules)
    },
    errorMessageId() {
      return this.inputId && `${this.inputId}-error`
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["textarea"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    validate() {
      const result = this.$refs["textarea"].validate()
      this.hasError = result !== true
      return result
    },
    resetValidation() {
      return this.$refs["textarea"].resetValidation()
    },
    assignInputId() {
      this.inputId = this.$refs?.["textarea"]?.$refs?.["input"].id
    },
  },
  mounted() {
    this.removeInnerLabel()
    this.assignInputId()
    if (this.form) this.form.register(this)
    else if (this.$attrs.rules?.length)
      console.warn(`component ${this.inputId} with validation rules not in a form, a11y markup may not work`)
  },
  beforeDestroy() {
    // https://github.com/vuetifyjs/vuetify/issues/3464#issuecomment-370240024
    if (this.form) this.form.unregister(this)
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
