<template>
  <div>
    <h1>Test DSFR</h1>
    <DsfrAlert title="Testing" />
    <span class="fr-icon-pencil-fill" aria-hidden="true"></span>
    <h2>Testing selects when migrating nos-cantines</h2>
    <v-select v-model="testSelect" :items="items" multiple clearable item-title="text">
      <!-- https://github.com/vuetifyjs/vuetify/issues/15721#issuecomment-1595860094 -->
      <template #item="{ item, props }">
        <v-divider v-if="'divider' in item.raw" class="pb-0" />
        <v-list-subheader v-else-if="'header' in item.raw" :title="item.raw.header" />
        <!-- include item.text for backwards compatibility old vuetify 2 code -->
        <v-list-item v-else>
          <v-checkbox
            v-bind="props"
            :label="item.raw.title || item.raw.text"
            :value="item.value"
            class="my-0 text-black"
            hide-details
            color="primary"
          />
        </v-list-item>
      </template>
    </v-select>
    <DsfrSelect v-model="testSelect" :items="items" multiple clearable></DsfrSelect>
    <DsfrSelect v-model="testSelect" :items="items"></DsfrSelect>
  </div>
</template>

<script>
import DsfrSelect from "@/components/DsfrSelect"

export default {
  name: "LandingPage",
  components: { DsfrSelect },
  data() {
    return {
      testSelect: [],
      items: [{ text: "test 1", value: 1 }, { header: "Header" }, { text: "test 2", value: 2 }],
    }
  },
}
</script>
