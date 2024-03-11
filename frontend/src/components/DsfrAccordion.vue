<template>
  <v-expansion-panels hover accordion tile flat>
    <v-expansion-panel v-for="item in items" :key="item.title">
      <v-expansion-panel-header class="px-3 fr-accordion__btn" v-slot="{ open }">
        <component :is="item.titleLevel || 'h3'" class="fr-text" :class="open && 'active-panel'">
          {{ item.title }}
        </component>
      </v-expansion-panel-header>
      <v-expansion-panel-content class="my-2">
        <component :is="item.contentComponent" v-if="item.contentComponent" />
        <p v-else-if="item.content" class="mb-0">{{ item.content }}</p>
        <slot v-else />
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "DsfrAccordion",
  props: {
    // items is an array of objects containing 'title'
    // and one of 'contentComponent', 'content', or falls back to a slot
    items: Array,
  },
}
</script>

<style>
.v-expansion-panel {
  box-shadow: inset 0 1px 0 0 #ddd, 0 1px 0 0 #ddd;
}
.v-expansion-panel-header {
  color: rgb(0, 0, 145);
}
.v-expansion-panel-header__icon > i {
  color: rgb(0, 0, 145) !important;
}
.v-expansion-panel--active > .v-expansion-panel-header {
  min-height: unset;
}
.fr-accordion__btn[aria-expanded="true"] {
  --background-open-blue-france: rgb(227, 227, 253);
  background-color: #e3e3fd;
  background-color: var(--background-open-blue-france);
}
.fr-accordion__btn[aria-expanded="true"]:hover {
  --background-open-blue-france-hover: rgb(193, 193, 251);
  background-color: var(--background-open-blue-france-hover);
}
</style>
