<template>
  <VueSelectCombobox
    v-if="options"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    label="Département"
    :labelClasses="labelClasses"
    :options="options"
    optionLabelKey="combinedName"
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
  },
  data() {
    const valueKey = "departmentCode"
    const nameKey = "departmentName"
    return {
      options: undefined,
      valueKey,
      nameKey,
    }
  },
  mounted() {
    this.options = this.sortedOptions()
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
      return this.selectableOptions?.indexOf(option[this.valueKey]) > -1
    },
    sortedOptions() {
      const unsortedOptions = jsonDepartments.map((d) => ({
        ...d,
        combinedName: `${d[this.valueKey]} - ${d[this.nameKey]}`,
      }))
      const options = JSON.parse(JSON.stringify(unsortedOptions))
      // TODO: add header message before unavailable options
      options.sort((optionA, optionB) => this.isOptionSelectable(optionB) - this.isOptionSelectable(optionA))
      return options
    },
  },
  watch: {
    selectableOptions() {
      this.options = this.sortedOptions()
    },
  },
}
</script>
