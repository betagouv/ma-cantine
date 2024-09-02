<template>
  <v-data-table :items="wasteActions" :headers="listHeaders" :hide-default-footer="true" :disable-sort="true">
    <template v-slot:[`item.title`]="{ item }">
      <router-link :to="{ name: 'WasteActionPage', params: { id: item.id } }">
        {{ item.title }}
      </router-link>
    </template>
    <template v-slot:[`item.effort`]="{ item }">
      <DsfrTag :text="effortDisplay(item.effort)" :small="true" :clickable="false" />
    </template>
    <template v-slot:[`item.wasteOrigins`]="{ item }">
      <div class="d-flex flex-wrap justify-end justify-sm-start mt-4 mb-2">
        <DsfrTag
          v-for="tag in item.wasteOrigins"
          :key="tag"
          :text="originsDisplay(tag)"
          :small="true"
          :clickable="false"
          class="ml-2 ml-sm-0 mr-sm-2 mb-2"
        />
      </div>
    </template>
  </v-data-table>
</template>

<script>
import DsfrTag from "@/components/DsfrTag"
import Constants from "@/constants"

export default {
  name: "WasteActionsListView",
  props: {
    wasteActions: {
      type: Array,
    },
  },
  components: { DsfrTag },
  data() {
    return {
      listHeaders: [
        { text: "Action", value: "title" },
        { text: "Description courte", value: "subtitle" },
        { text: "Taille", value: "effort", width: "15%" },
        { text: "Source", value: "wasteOrigins", width: "20%" },
      ],
    }
  },
  methods: {
    effortDisplay(level) {
      return Constants.WasteActionEffortLevels.find((item) => item.value === level)?.text
    },
    originsDisplay(origin) {
      return Constants.WasteActionOrigins.find((item) => item.value === origin)?.text
    },
  },
}
</script>
