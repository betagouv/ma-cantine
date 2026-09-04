<template>
  <v-radio-group class="my-0" ref="radiogroup" v-bind="$attrs" v-on="$listeners" @change="change">
    <template v-slot:label>
      <span class="d-block">
        <span :class="legendClass">
          {{ $attrs.label }}
        </span>
        <span v-if="optional" class="fr-hint-text mb-2">Optionnel</span>
      </span>
    </template>
    <v-row v-if="optionsRow" class="my-0">
      <v-col cols="12" sm="6" class="py-2" v-for="item in items" :key="item.value">
        <v-radio :value="item.value" :class="optionClasses">
          <template v-slot:label>
            <span :class="optionClasses">
              {{ item.label || item.text }}
            </span>
          </template>
        </v-radio>
      </v-col>
    </v-row>
    <v-radio v-else v-for="item in items" :key="item.value" :value="item.value" :class="optionClasses">
      <template v-slot:label>
        <span :class="optionClasses">
          {{ item.label || item.text }}
        </span>
      </template>
    </v-radio>

    <!-- For RGAA 8.9 error messages should also be in p tags, by default in vuetify 2 they're in divs -->
    <template v-slot:message="{ key, message }">
      <p :id="errorMessageId" :key="key" class="mb-0">{{ message }}</p>
    </template>
  </v-radio-group>
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
      type: [String, Object],
    },
    optionClasses: {
      type: String,
      default: "",
    },
    hideOptional: {
      default: false,
    },
    yesNo: {
      type: Boolean,
      default: false,
    },
    optionsRow: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return { inputId: null }
  },
  computed: {
    value() {
      return this.$refs["radiogroup"].value
    },
    reset() {
      return this.$refs["radiogroup"].reset
    },
    items() {
      if (this.yesNo) {
        return [
          { label: "Oui", value: true },
          { label: "Non", value: false },
        ]
      }
      return this.$attrs["items"]
    },
    legendClass() {
      if (this.labelClasses) return this.labelClasses
      const activeColor = " grey--text text--darken-4"
      const inactiveColor = " grey--text"
      const color = this.$attrs.disabled ? inactiveColor : activeColor
      const defaultClasses = "mb-2 text-sm-subtitle-1 text-body-2 text-left d-block"
      return defaultClasses + color
    },
    optional() {
      return !this.hideOptional && !validators._includesRequiredValidator(this.$attrs.rules)
    },
    errorMessageId() {
      return `${this.inputId}-error`
    },
  },
  methods: {
    change(v) {
      this.$emit("input", v)
      this.validate()
    },
    validate() {
      const result = this.$refs["radiogroup"].validate()
      this.hasError = result !== true
      this.assignValidity()
      return result
    },
    resetValidation() {
      return this.$refs["radiogroup"].resetValidation()
    },
    assignInputId() {
      this.inputId = this.$refs?.["radiogroup"]?.$refs?.["label"].id
    },
    assignDescribedby() {
      this.$refs["radiogroup"].$el
        .querySelector("[role=radiogroup]")
        .setAttribute("aria-describedby", this.errorMessageId)
    },
    assignValidity() {
      this.$refs["radiogroup"].$el.querySelector("[role=radiogroup]").setAttribute("aria-invalid", this.hasError)
    },
  },
  mounted() {
    this.assignInputId()
    this.assignDescribedby()
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
.v-radio >>> label {
  color: inherit;
}
</style>
