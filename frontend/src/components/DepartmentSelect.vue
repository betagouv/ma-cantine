<template>
  <VueSelectCombobox
    v-model="department"
    label="Département"
    :labelClasses="labelClasses"
    :options="options"
    optionLabelKey="combinedName"
    :optionValueKey="valueKey"
    :filterBy="filterBy"
    noOptionsText="Pas de départements qui correspondent à la recherche"
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
  },
  data() {
    const valueKey = "departmentCode"
    const nameKey = "departmentName"
    return {
      department: undefined, // TODO: initisalise with parent value
      options: jsonDepartments.map((d) => ({
        ...d,
        combinedName: `${d[valueKey]} - ${d[nameKey]}`,
      })),
      valueKey,
      nameKey,
    }
  },
  methods: {
    // TODO: make it possible to make options unavailable
    filterBy(option, label, search) {
      const normalisedSearch = normaliseText(search)
      const searchMatchesCode =
        normaliseText(option[this.valueKey]) === normalisedSearch || +option[this.valueKey] === +search
      if (searchMatchesCode) {
        return true
      }
      return normaliseText(option[this.nameKey] || "").indexOf(normalisedSearch) === 0
    },
  },
  watch: {
    department() {
      this.$emit("input", this.department)
    },
  },
}
</script>
