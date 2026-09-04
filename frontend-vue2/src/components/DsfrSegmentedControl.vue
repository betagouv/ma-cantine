<template>
  <fieldset :class="{ 'fr-segmented': true, 'fr-segmented--no-legend': noLegend }">
    <legend class="fr-segmented__legend">{{ legend }}</legend>
    <div class="fr-segmented__elements">
      <div v-for="item in itemsForDisplay" :key="item.value" class="fr-segmented__element">
        <input
          :value="item.value"
          type="radio"
          :id="`segmented-${item.value}`"
          :name="name"
          v-on:input="$emit('input', $event.target.value)"
          :checked="value === item.value"
          :disabled="item.disabled"
        />
        <label class="fr-label" :for="`segmented-${item.value}`">
          <v-icon v-if="item.icon" small class="mr-2">{{ item.icon }}</v-icon>
          {{ item.text }}
        </label>
      </div>
    </div>
  </fieldset>
</template>

<script>
export default {
  name: "DsfrSegmentedControl",
  props: {
    value: [String, Number],
    legend: String, // necessary even if not displayed
    noLegend: Boolean,
    // array of text value objects
    items: Array,
    name: {
      type: String,
      default: "segmented-group",
    },
  },
  computed: {
    itemsForDisplay() {
      if (!this.items.length) return this.items
      if (this.items[0].text) return this.items
      return this.items.map((i) => ({ text: i, value: i }))
    },
  },
}
</script>

<style lang="scss" scoped>
/* TODO: styling for SM as well as MD */
.fr-segmented {
  align-items: center;
  border: 0;
  display: inline-flex;
  margin: 0;
  padding: 0;
  position: relative;
}
.fr-segmented__legend {
  margin-bottom: 0.75rem;
  padding: 0;
}
.fr-segmented--no-legend legend {
  clip: rect(0, 0, 0, 0);
  border: 0;
  display: block;
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
.fr-segmented--no-legend legend + .fr-segmented__elements {
  margin-left: 0;
}
.fr-segmented__elements {
  border-radius: 0.25rem;
  box-shadow: inset 0 0 0 1px #ddd;
  // box-shadow: inset 0 0 0 1px var(--border-default-grey);
  display: flex;
  flex-direction: row;
}
.fr-segmented__element {
  position: relative;
}
.fr-segmented input {
  height: 100%;
  margin: 0;
  position: absolute;
  width: 100%;
  z-index: -1;
}
.fr-segmented input:disabled + label {
  --text-disabled-grey: rgb(146, 146, 146);
  color: var(--text-disabled-grey);
  cursor: not-allowed;
}
.fr-segmented input + label {
  align-items: center;
  border-radius: 0.25rem;
  display: inline-flex;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5rem;
  max-height: none;
  max-width: 100%;
  min-height: 2.5rem;
  overflow: visible;
  overflow: initial;
  padding: 0.5rem 1rem;
  white-space: nowrap;
  width: 100%;
}
.fr-segmented input + label::before {
  --icon-size: 1rem;
  margin-left: -0.125rem;
  margin-right: 0.5rem;
}
.fr-segmented .fr-segmented__element input {
  opacity: 0;
}
// TODO: fix focus styling, currently not displayed for some reason
input:focus {
  outline-color: #0a76f6;
  outline-offset: 2px;
  outline-style: solid;
  outline-width: 2px;
}
// TODO: why is background hover taking up whole space when in DSFR it leaves some space?
.fr-segmented input:not([disabled]):not(:checked) + label:hover {
  --grey-1000-50-hover: #f6f6f6;
  --grey-1000-50-active: #ededed;
  --background-default-grey-hover: var(--grey-1000-50-hover);
  --background-default-grey-active: var(--grey-1000-50-active);
  --hover: var(--background-default-grey-hover);
  --active: var(--background-default-grey-active);
  background-color: var(--hover);
}
.fr-segmented__element input:checked + label {
  box-shadow: inset 0 0 0 1px #000091;
  // box-shadow: inset 0 0 0 1px var(--border-active-blue-france);
  color: #000091;
  // color: var(--text-active-blue-france);
}
input:focus + label {
  outline-color: #0a76f6;
  outline-offset: 2px;
  outline-style: solid;
  outline-width: 2px;
}
label > span {
  color: inherit !important;
}
</style>
