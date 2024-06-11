<template>
  <VueSelectCombobox
    v-if="options"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    label="Département"
    :labelClasses="labelClasses"
    :options="options"
    optionLabelKey="text"
    :optionValueKey="valueKey"
    :filterBy="filterBy"
    noOptionsText="Pas de départements qui correspondent à la recherche"
    :selectable="isOptionSelectable"
  />
</template>

<script>
import VueSelectCombobox from "./VueSelectCombobox"
import jsonDepartments from "@/departments.json"
import { normaliseText } from "@/utils"

export default {
  name: "DepartmentSelect",
  components: { VueSelectCombobox },
  props: {
    labelClasses: {
      type: [String, Object],
      default: "",
    },
    selectableOptions: {
      type: Array,
      required: false,
    },
    unselectableOptionsHeader: {
      type: String,
      default: "Les options suivantes ne sont pas disponibles",
    },
  },
  data() {
    const valueKey = "departmentCode"
    const nameKey = "departmentName"
    return {
      valueKey,
      nameKey,
    }
  },
  methods: {
    filterBy(option, label, search) {
      const normalisedSearch = normaliseText(search)
      const searchMatchesCode =
        normaliseText(option[this.valueKey]) === normalisedSearch || +option[this.valueKey] === +search
      if (searchMatchesCode) {
        return true
      }
      return normaliseText(option[this.nameKey] || "").indexOf(normalisedSearch) === 0
    },
    isOptionSelectable(option) {
      if (this.selectableOptions === undefined) return true
      return this.selectableOptions.indexOf(option[this.valueKey]) > -1
    },
  },
  computed: {
    options() {
      const unsortedOptions = jsonDepartments.map((d) => ({
        ...d,
        text: `${d[this.valueKey]} - ${d[this.nameKey]}`,
      }))
      if (this.selectableOptions === undefined) return unsortedOptions
      if (!this.selectableOptions.length) return []

      const availableOptions = unsortedOptions.filter((opt) => this.selectableOptions.indexOf(opt[this.valueKey]) > -1)
      const unavailableOptions = unsortedOptions.filter(
        (opt) => this.selectableOptions.indexOf(opt[this.valueKey]) === -1
      )
      let options = []
      if (availableOptions.length) options = options.concat(availableOptions)
      if (unavailableOptions.length) {
        options.push({ text: this.unselectableOptionsHeader })
        options = options.concat(unavailableOptions)
      }
      return options
    },
  },
}
</script>
