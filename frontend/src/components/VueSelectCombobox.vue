<template>
  <div class="mc-select">
    <label>{{ label }}</label>
    <VueSelect
      :id="wrapperId"
      v-model="selected"
      :options="options"
      :label="optionLabelKey"
      :selectOnTab="true"
      :filterBy="filterBy"
    />
  </div>
</template>

<script>
import { VueSelect } from "vue-select"
import "vue-select/dist/vue-select.css"

// TODO: dsfr styling

export default {
  name: "VueSelectCombobox",
  components: { VueSelect },
  props: {
    label: {
      type: String,
      required: true,
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
  },
  data() {
    const number = Math.floor(Math.random() * 1000)
    const wrapperId = `mc-combobox-${number}`
    return {
      selected: undefined, // TODO: how to initialise with parent v-model value?
      wrapperId,
    }
  },
  mounted() {
    const vueSelect = document.getElementById(this.wrapperId)
    const combobox = vueSelect.querySelector("[role=combobox]")
    // replace the default aria-label provided by the library
    combobox.setAttribute("aria-label", this.label)
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
</style>
