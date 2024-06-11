<template>
  <div class="mc-select">
    <label :class="labelClasses">{{ label }}</label>
    <VueSelect
      :id="wrapperId"
      v-model="selected"
      :options="options"
      :label="optionLabelKey"
      :selectOnTab="true"
      :filterBy="filterBy"
      placeholder="Selectionner une option"
      class="mt-1"
      :selectable="selectable"
    >
      <template #no-options>
        {{ noOptionsText }}
      </template>
    </VueSelect>
  </div>
</template>

<script>
import { VueSelect } from "vue-select"
import "vue-select/dist/vue-select.css"

// TODO: validation

export default {
  name: "VueSelectCombobox",
  components: { VueSelect },
  props: {
    label: {
      type: String,
      required: true,
    },
    labelClasses: {
      type: [String, Object],
      default: "",
    },
    options: {
      type: Array,
      required: true,
    },
    optionLabelKey: {
      type: String,
      default: "label",
    },
    optionValueKey: {
      type: String,
      default: "value",
    },
    filterBy: {
      type: Function,
      // https://vue-select.org/api/props.html#filterby
      default(option, label, search) {
        return (label || "").toLocaleLowerCase().indexOf(search.toLocaleLowerCase()) > -1
      },
    },
    noOptionsText: {
      type: String,
      default: "Pas d'options qui correspondent à la recherche",
    },
    selectable: {
      type: Function,
      default() {
        return true
      },
    },
  },
  data() {
    const number = Math.floor(Math.random() * 1000)
    const wrapperId = `mc-combobox-${number}`
    return {
      selected: undefined,
      wrapperId,
    }
  },
  mounted() {
    const vueSelect = document.getElementById(this.wrapperId)
    const combobox = vueSelect.querySelector("[role=combobox]")
    // replace the default aria-label provided by the library
    combobox.setAttribute("aria-label", this.label)
    const clearButton = vueSelect.querySelector("button.vs__clear")
    clearButton.setAttribute("title", "Supprimer la selection")
    clearButton.setAttribute("aria-label", "Supprimer la selection")
    // modify display of clear button icon, taking advantage of vuetify classes
    clearButton.innerHTML = ""
    const clearButtonClasses = "v-icon v-icon--link mdi mdi-close primary--text mr-5"
    clearButtonClasses.split(" ").forEach((className) => clearButton.classList.add(className))
    // replace open indicator with background image like NativeSelect
    const vueSelectDropdownIndicator = vueSelect.querySelector("svg.vs__open-indicator")
    vueSelectDropdownIndicator.remove()
    // initisalise value
    this.$nextTick(() => {
      const originalValue = this.$attrs.value
      this.selected = this.options.find((o) => o[this.optionValueKey] === originalValue)
    })
  },
  watch: {
    selected() {
      this.$emit("input", this.selected?.[this.optionValueKey])
    },
  },
}
</script>

<style>
.vs__dropdown-menu {
  padding-left: 0px !important;
}
.vs__dropdown-toggle {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  transition: none;
  height: 38px;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23161616' d='m12 13.1 5-4.9 1.4 1.4-6.4 6.3-6.4-6.4L7 8.1l5 5z'/%3E%3C/svg%3E");
  background-position: calc(100% - 1rem) 50%;
  background-repeat: no-repeat;
  background-size: 1rem 1rem;
  border: none;
  padding-left: 6px;
  padding-right: 12px;
}
li.vs__dropdown-option {
  white-space: normal;
}
</style>
