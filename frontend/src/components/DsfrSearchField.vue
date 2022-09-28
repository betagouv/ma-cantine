<template>
  <DsfrTextField
    :placeholder="$attrs['placeholder'] || 'Rechercher'"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    clearable
    @click:clear="clearAction"
    @keyup.enter="searchAction"
    ref="text-field"
  >
    <template v-slot:append>
      <button class="fr-btn mr-n3" title="Rechercher">
        Rechercher
      </button>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "@/components/DsfrTextField"

export default {
  inheritAttrs: false,
  components: { DsfrTextField },
  props: ["searchAction", "clearAction"],
  computed: {
    lazyValue() {
      return this.$refs["text-field"].lazyValue
    },
    value() {
      return this.$refs["text-field"].value
    },
  },
  methods: {
    validate() {
      return this.$refs["text-field"].validate()
    },
  },
}
</script>

<style scoped>
.fr-btn::before {
  --icon-size: 1.5rem;
  background-color: currentColor;
  content: "";
  display: inline-block;
  flex: 0 0 auto;
  height: var(--icon-size);
  margin-left: -0.5rem; /* customised */
  margin-right: 0.5rem;
  -webkit-mask-image: url("/static/icons/search-line.svg");
  mask-image: url("/static/icons/search-line.svg");
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
  vertical-align: calc(0.375em - var(--icon-size) * 0.5);
  width: var(--icon-size);
}
.fr-btn {
  /* variables */
  --blue-france-sun-113-625: #000091;
  --blue-france-sun-113-625-hover: #1212ff;
  --blue-france-sun-113-625-active: #2323ff;
  --blue-france-975-sun-113: #f5f5fe;
  --background-action-high-blue-france: var(--blue-france-sun-113-625);
  --background-action-high-blue-france-hover: var(--blue-france-sun-113-625-hover);
  --background-action-high-blue-france-active: var(--blue-france-sun-113-625-active);
  --text-inverted-blue-france: var(--blue-france-975-sun-113);
  /* search-bar */
  border-radius: 0 0.25rem 0 0;
  flex: 1 0 auto;
  font-size: 1rem;
  line-height: 1.5rem;
  max-height: 2.5rem;
  max-width: 2.5rem;
  min-height: 2.5rem;
  overflow: hidden;
  padding: 0.5rem;
  white-space: nowrap;
  /* general btn */
  --text-spacing: 0;
  --title-spacing: 0;
  --underline-img: none;
  --hover-tint: var(--hover);
  --idle: transparent;
  --hover: var(--background-action-high-blue-france-hover);
  --active: var(--background-action-high-blue-france-active);
  align-items: center;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  display: inline-flex;
  flex-direction: row;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5rem;
  min-height: 2.5rem;
  padding: 0.5rem 1rem;
  width: -moz-fit-content;
  width: -webkit-fit-content;
  width: fit-content;
  z-index: 1;
}
.fr-btn:hover {
  --blue-france-sun-113-625-hover: #1212ff;
  --background-action-high-blue-france-hover: var(--blue-france-sun-113-625-hover);
  background-color: var(--background-action-high-blue-france-hover);
}
</style>
