<template>
  <div>
    <GenericMeasureResults :badge="badge" :canteen="canteen" :diagnostics="diagnostics" />
    <v-row v-if="canteenResourceActionsDone.length" class="mb-2">
      <v-col
        vols="12"
        sm="6"
        md="4"
        v-for="resourceAction in canteenResourceActionsDone"
        :key="resourceAction.resource.id"
      >
        <WasteActionCard :wasteAction="resourceAction.resource" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"
import WasteActionCard from "@/components/WasteActionCard"

export default {
  name: "WasteMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnostics: Array,
    editable: Boolean,
  },
  components: { GenericMeasureResults, WasteActionCard },
  computed: {
    canteenResourceActionsDone() {
      return this.canteen?.resourceActions ? this.canteen.resourceActions.filter((ra) => ra.isDone) : []
    },
  },
}
</script>
