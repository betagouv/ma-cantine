<template>
  <div :class="{ 'fr-toggle': true, 'fr-toggle--label-left': labelLeft }" @click.self="clickInput">
    <input
      :disabled="disabled"
      :aria-disabled="disabled"
      type="checkbox"
      :checked="value"
      class="fr-toggle__input"
      aria-describedby="toggle-698-hint-text"
      @input="$emit('input', $event.target.checked)"
      ref="toggle"
    />
    <label
      class="fr-toggle__label"
      for="toggle-698"
      :data-fr-checked-label="checkedLabel"
      :data-fr-unchecked-label="uncheckedLabel"
      @click.self="clickInput"
    >
      <span v-if="label">{{ label }}</span>
      <span class="pr-2"><slot name="label" /></span>
    </label>
    <p v-if="hint" class="fr-hint-text" id="toggle-698-hint-text">{{ hint }}</p>
  </div>
</template>

<script>
export default {
  name: "DsfrToggle",
  props: {
    // TODO: add value, set publication status as boolean in model
    // TODO: programmatic id
    value: Boolean,
    label: {
      type: String,
      optional: true,
    },
    labelLeft: {
      type: Boolean,
      default: false,
    },
    checkedLabel: {
      type: String,
      default: "Activé",
    },
    uncheckedLabel: {
      type: String,
      default: "Désactivé",
    },
    hint: {
      type: String,
      optional: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    clickInput() {
      this.$refs.toggle.click()
    },
  },
}
</script>

<style scoped>
.fr-toggle {
  --text-spacing: 0;
  --title-spacing: 0;
  display: flex;
  flex-wrap: wrap;
  padding: 1rem 0;
  position: relative;
}
.fr-toggle input[type="checkbox"] {
  box-shadow: inset 0 0 0 1px #000091;
  /* box-shadow: inset 0 0 0 1px var(--border-action-high-blue-france); */
  height: 1.5rem;
  opacity: 0;
  position: absolute;
  width: 2.5rem;
}
.fr-toggle label::after {
  --idle: transparent;
  --grey-1000-50-hover: #f6f6f6;
  --grey-1000-50-active: #ededed;
  --background-default-grey-hover: var(--grey-1000-50-hover);
  --background-default-grey-active: var(--grey-1000-50-active);
  --hover: var(--background-default-grey-hover);
  --active: var(--background-default-grey-active);
  align-items: center;
  background-color: #fff;
  /* background-color: var(--background-default-grey); */
  background-position: 50%;
  background-size: 1rem;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px #000091;
  /* box-shadow: inset 0 0 0 1px var(--border-action-high-blue-france); */
  display: flex;
  height: 1.5rem;
  justify-content: center;
  left: 0;
  position: absolute;
  top: 1rem;
  width: 1.5rem;
}
.fr-toggle label::after,
.fr-toggle label::before {
  background-repeat: no-repeat;
  color: #000091;
  /* color: var(--text-active-blue-france); */
  content: "";
}
.fr-toggle label[data-fr-unchecked-label][data-fr-checked-label]::before {
  content: attr(data-fr-unchecked-label);
  margin-bottom: 1rem;
  margin-right: calc(var(--toggle-status-width) - 0.5rem);
}
.fr-toggle label::before {
  --data-uri-svg: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='24' fill='transparent' stroke='%23000091'%3E%3Crect width='39' height='23' x='.5' y='.5' rx='11.5'/%3E%3C/svg%3E");
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='24' fill='transparent' stroke='%23000091'%3E%3Crect width='39' height='23' x='.5' y='.5' rx='11.5'/%3E%3C/svg%3E");
  background-image: var(--data-uri-svg);
  border-radius: 0.75rem;
  display: block;
  flex-shrink: 0;
  font-size: 0.75rem;
  height: calc(1.25rem + 1px);
  line-height: 1.25rem;
  margin-right: 2rem;
  max-width: 2.5rem;
  min-width: 2.5rem;
  padding-top: 1.75rem;
}
.fr-toggle label[data-fr-unchecked-label][data-fr-checked-label] {
  padding-left: 0;
}
input[type="checkbox"] {
  cursor: pointer;
}
input[type="checkbox"] + label {
  cursor: pointer;
}
.fr-toggle label {
  --toggle-status-width: 2.5rem;
  color: #161616;
  /* color: var(--text-label-grey); */
  display: inline-flex;
  font-size: 1rem;
  line-height: 1.5rem;
  min-height: 1.5rem;
  width: calc(100% - 2rem);
}
.fr-toggle label[data-fr-unchecked-label][data-fr-checked-label] + .fr-hint-text {
  margin-top: 0.5rem;
}
.fr-toggle .fr-hint-text {
  color: #666;
  /* color: var(--text-mention-grey); */
  display: block;
  flex-basis: 100%;
  font-size: 0.75rem;
  line-height: 1.25rem;
  margin-bottom: 0;
  margin-top: 1rem;
}
.fr-toggle--label-left .fr-toggle__input + label[data-fr-checked-label]::before {
  margin-left: calc(var(--toggle-status-width) - 0.5rem);
  margin-right: 0;
}
.fr-toggle--label-left .fr-toggle__label::before {
  direction: rtl;
  flex-shrink: 0;
  margin-left: 1rem;
  margin-right: 0;
  order: 1;
  text-align: right;
}
.fr-toggle--label-left .fr-toggle__label {
  flex: 1;
  justify-content: space-between;
  padding-left: 0;
  width: calc(100% - 2rem);
}
.fr-toggle--label-left .fr-toggle__label::after {
  left: auto;
  right: 1rem;
}
.fr-toggle input[type="checkbox"]:checked {
  --idle: transparent;
  --hover: var(--background-active-blue-france-hover);
  --active: var(--background-active-blue-france-active);
  background-color: #000091;
  /* background-color: var(--background-active-blue-france); */
}
.fr-toggle input[type="checkbox"]:checked ~ .fr-toggle__label::after {
  /* --data-uri-svg: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000091' d='m10 15.17 9.2-9.2 1.4 1.42L10 18l-6.36-6.36 1.4-1.42z'/%3E%3C/svg%3E"); */
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000091' d='m10 15.17 9.2-9.2 1.4 1.42L10 18l-6.36-6.36 1.4-1.42z'/%3E%3C/svg%3E");
  /* background-image: var(--data-uri-svg); */
  transform: translateX(1rem);
}
.fr-toggle input[type="checkbox"]:checked ~ .fr-toggle__label[data-fr-unchecked-label][data-fr-checked-label]::before {
  content: attr(data-fr-checked-label);
}
.fr-toggle
  input[type="checkbox"]:not(:checked)
  ~ .fr-toggle__label[data-fr-unchecked-label][data-fr-checked-label]::before {
  content: attr(data-fr-unchecked-label);
}
.fr-toggle input[type="checkbox"]:checked ~ .fr-toggle__label::before {
  --data-uri-svg: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='24' fill='%23000091' stroke='%23000091'%3E%3Crect width='39' height='23' x='.5' y='.5' rx='11.5'/%3E%3C/svg%3E");
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='24' fill='%23000091' stroke='%23000091'%3E%3Crect width='39' height='23' x='.5' y='.5' rx='11.5'/%3E%3C/svg%3E");
  background-image: var(--data-uri-svg);
}
input[type="checkbox"]:focus + label::before {
  outline-color: #0a76f6;
  outline-offset: 2px;
  outline-style: solid;
  outline-width: 2px;
}
</style>
