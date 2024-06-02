<template>
  <div>
    <label :for="inputId" :class="labelClasses" v-if="$attrs.label">
      {{ $attrs.label }}
    </label>
    <v-autocomplete
      dense
      min-height="40"
      ref="autocomplete"
      solo
      flat
      v-bind="$attrs"
      v-on="$listeners"
      persistent-placeholder
      @input="(v) => $emit('input', v)"
      :aria-describedby="errorMessageId"
      auto-select-first
      :search-input.sync="searchInput"
      @change="searchInput = ''"
      :filter="unaccentedFilter"
    >
      <template v-slot:label><span></span></template>

      <!-- For RGAA 8.9 error messages should also be in p tags, by default in vuetify 2 they're in divs -->
      <template v-slot:message="{ key, message }">
        <p :id="errorMessageId" :key="key" class="mb-0">{{ message }}</p>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
import { normaliseText } from "@/utils"
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
    return {
      searchInput: null,
      inputId: null,
    }
  },
  computed: {
    errorMessageId() {
      return this.inputId && `${this.inputId}-error`
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["autocomplete"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    assignInputId() {
      this.inputId = this.$refs?.["autocomplete"]?.$refs?.["input"].id
    },
    unaccentedFilter(item, queryText, itemText) {
      const normalizedQueryText = normaliseText(queryText).toLocaleLowerCase()
      const normalizedItemText = normaliseText(itemText).toLocaleLowerCase()
      return normalizedItemText.indexOf(normalizedQueryText) > -1
    },
  },
  mounted() {
    this.removeInnerLabel()
    this.assignInputId()
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
