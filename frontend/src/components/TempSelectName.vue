<template>
  <div>
    <label :for="inputId" :class="labelClasses">{{ label }}</label>
    <select
      ref="select"
      :id="inputId"
      v-bind:value="value"
      v-on:input="$emit('input', $event.target.value)"
      class="fr-select"
    >
      <option v-for="item in items" :key="item.value" :value="item.value">
        {{ item.text }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "TempSelectName",
  props: {
    value: String,
    items: {
      // array of objects with value and text
      type: Array,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    labelClasses: {
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left",
    },
  },
  data() {
    return { inputId: null }
  },
  methods: {
    assignInputId() {
      const randInt = Math.floor(Math.random() * 1000)
      this.inputId = `select-${randInt}`
    },
    updateModel(event) {
      console.log(event.target)
      console.log(event.target.value)
      this.$emit("input", event.target.value)
    },
  },
  mounted() {
    this.assignInputId()
  },
}
</script>

<style lang="scss" scoped>
label {
  display: block;
}
select.fr-select {
  --grey-950-100: #eee;
  --grey-950-100-hover: #d2d2d2;
  --grey-950-100-active: #c1c1c1;
  --grey-200-850: #3a3a3a;
  --background-contrast-grey: var(--grey-950-100);
  --background-contrast-grey-hover: var(--grey-950-100-hover);
  --background-contrast-grey-active: var(--grey-950-100-active);
  --border-plain-grey: var(--grey-200-850);
  --text-default-grey: var(--grey-200-850);
  --idle: transparent;
  --hover: var(--background-contrast-grey-hover);
  --active: var(--background-contrast-grey-active);
  --data-uri-svg: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23161616' d='m12 13.1 5-4.9 1.4 1.4-6.4 6.3-6.4-6.4L7 8.1l5 5z'/%3E%3C/svg%3E");
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: #eee;
  background-color: var(--background-contrast-grey);
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23161616' d='m12 13.1 5-4.9 1.4 1.4-6.4 6.3-6.4-6.4L7 8.1l5 5z'/%3E%3C/svg%3E");
  background-image: var(--data-uri-svg);
  background-position: calc(100% - 1rem) 50%;
  background-repeat: no-repeat;
  background-size: 1rem 1rem;
  border-radius: 0.25rem 0.25rem 0 0;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  box-shadow: inset 0 -2px 0 0 var(--border-plain-grey);
  color: #3a3a3a;
  color: var(--text-default-grey);
  display: block;
  font-size: 1rem;
  line-height: 1.5rem;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  width: 100%;
}
</style>
