<template>
  <div>
    <component v-if="heading" :is="headingLevel" :id="headingId" :class="headingClasses">{{ heading }}</component>
    <VueApexCharts v-bind="$attrs" :aria-labelledBy="headingId" :aria-describedby="descriptionId" />
    <DsfrAccordion :items="[{ title: 'Description du graphique' }]" class="mb-2">
      <div :id="descriptionId">
        <slot name="description"></slot>
      </div>
    </DsfrAccordion>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import DsfrAccordion from "@/components/DsfrAccordion"

export default {
  name: "GraphComponent",
  props: {
    graphId: {
      type: String,
      required: true,
    },
    heading: String,
    headingLevel: {
      type: String,
      default: "h2",
    },
    headingClasses: {
      type: String,
      default: "",
    },
  },
  components: {
    VueApexCharts,
    DsfrAccordion,
  },
  computed: {
    headingId() {
      return this.graphId + "-heading"
    },
    descriptionId() {
      return this.graphId + "-description"
    },
  },
}
</script>
