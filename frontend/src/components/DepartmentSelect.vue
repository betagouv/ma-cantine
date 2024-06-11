<template>
  <VueSelectCombobox
    v-model="department"
    label="Département"
    :options="options"
    optionLabelKey="combinedName"
    :optionValueKey="valueKey"
    :filterBy="filterBy"
  />
</template>

<script>
import VueSelectCombobox from "./VueSelectCombobox"
import jsonDepartments from "@/departments.json"
import { normaliseText } from "@/utils"

export default {
  name: "DepartmentSelect",
  components: { VueSelectCombobox },
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
