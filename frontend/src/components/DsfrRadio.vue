<template>
  <v-radio-group class="my-0" ref="radio" v-bind="$attrs" v-on="$listeners" @change="(v) => $emit('input', v)">
    <template v-slot:label>
      <span :class="labelClasses">
        {{ $attrs.label }}
      </span>
      <span class="fr-hint-text my-2" v-if="optional">Optionnel</span>
    </template>
    <v-row v-if="optionsRow">
      <v-col v-for="item in items" :key="item.value">
        <v-radio :label="item.label || item.text" :value="item.value"></v-radio>
      </v-col>
    </v-row>
    <v-radio
      v-else
      v-for="item in items"
      :key="item.value"
      :label="item.label || item.text"
      :value="item.value"
    ></v-radio>

    <!-- For RGAA 8.9 error messages should also be in p tags, by default in vuetify 2 they're in divs -->
    <template v-slot:message="{ key, message }">
      <p :key="key">{{ message }}</p>
    </template>
  </v-radio-group>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    labelClasses: {
      type: String,
      required: false,
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left grey--text text--darken-4",
    },
    optional: {
      type: Boolean,
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
