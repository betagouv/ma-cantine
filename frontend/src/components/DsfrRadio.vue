<template>
  <v-radio-group class="my-0" ref="radio" v-bind="$attrs" v-on="$listeners" @change="(v) => $emit('input', v)">
    <template v-slot:label>
      <span class="d-block mb-2">
        <span :class="legendClass">
          {{ $attrs.label }}
        </span>
        <span v-if="optional" class="fr-hint-text">Optionnel</span>
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
      <p :key="key" class="mb-0">{{ message }}</p>
    </template>
  </v-radio-group>
</template>

<script>
import validators from "@/validators"

export default {
  inheritAttrs: false,
  props: {
    labelClasses: {
      type: String,
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left d-block",
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
      return this.$refs["radio"].value
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
      const activeColor = " grey--text text--darken-4"
      const inactiveColor = " grey--text"
      const color = this.$attrs.disabled ? inactiveColor : activeColor
      return this.labelClasses + color
    },
    optional() {
      return !this.hideOptional && !validators._includesRequiredValidator(this.$attrs.rules)
    },
  },
  methods: {
    validate() {
      return this.$refs["radio"].validate()
    },
  },
}
</script>

<style scoped>
.v-radio >>> label {
  color: inherit;
}
</style>
