<template>
  <v-data-table :items="actionsDisplay" :headers="listHeaders" :hide-default-footer="true" :disable-sort="true">
    <template v-slot:[`item.title`]="{ item }">
      <router-link :to="{ name: 'WasteActionPage', params: { id: item.id } }">
        {{ item.title }}
      </router-link>
    </template>
    <template v-slot:[`item.effort`]="{ item }">
      <DsfrTag :text="item.effort.text" :icon="item.effort.icon" :small="true" :clickable="false" />
    </template>
    <template v-slot:[`item.wasteOrigins`]="{ item }">
      <div class="d-flex flex-wrap justify-end justify-sm-start my-2">
        <DsfrTag
          v-for="tag in item.wasteOrigins"
          :key="tag.text"
          :text="tag.text"
          :icon="tag.icon"
          :small="true"
          :clickable="false"
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
  computed: {
    actionsDisplay() {
      return this.wasteActions.map((a) => {
        return {
          id: a.id,
          title: a.title,
          subtitle: a.subtitle,
          effort: Constants.WasteActionEffortLevels.find((item) => item.value === a.effort),
          wasteOrigins: a.wasteOrigins.map((origin) =>
            Constants.WasteActionOrigins.find((item) => item.value === origin)
          ),
        }
      })
    },
  },
}
</script>
