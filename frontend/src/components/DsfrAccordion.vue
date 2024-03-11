<template>
  <v-expansion-panels hover accordion tile flat>
    <v-expansion-panel v-for="item in items" :key="item.title">
      <v-expansion-panel-header class="px-3" expand-icon="mdi-plus" disable-icon-rotate v-slot="{ open }">
        <h3 class="fr-text" :class="open && 'font-weight-bold'">
          {{ item.title }}
        </h3>
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
</style>
