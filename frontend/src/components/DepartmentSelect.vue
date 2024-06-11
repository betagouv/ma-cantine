<template>
  <VueSelectCombobox
    v-model="department"
    label="Département"
    :options="options"
    optionLabelKey="departmentName"
    :optionValueKey="valueKey"
    :filterBy="filterBy"
  />
</template>

<script>
import VueSelectCombobox from "./VueSelectCombobox"
import jsonDepartments from "@/departments.json"

export default {
  name: "DepartmentSelect",
  components: { VueSelectCombobox },
  data() {
    return {
      department: undefined, // TODO: initisalise with parent value
      options: jsonDepartments,
      valueKey: "departmentCode",
    }
  },
  methods: {
    filterBy(option, label, search) {
      const codeSearch = +search
      const searchMatchesCode = option[this.valueKey] === search || +option[this.valueKey] === codeSearch
      if (codeSearch && searchMatchesCode) {
        return true
      }
      return (label || "").toLocaleLowerCase().indexOf(search.toLocaleLowerCase()) > -1
    },
  },
  watch: {
    department() {
      this.$emit("input", this.department)
    },
  },
}
</script>
