<template>
  <div role="figure" :aria-labelledBy="headingId" :aria-label="label" :aria-describedby="descriptionId">
    <component v-if="heading" :is="headingLevel" :id="headingId" :class="headingClasses">{{ heading }}</component>
    <VueApexCharts v-bind="$attrs" />
    <DsfrAccordion :items="[{ title: 'Description du graphique' }]" class="mb-2">
      <template v-slot:content>
        <div :id="descriptionId">
          <slot name="description"></slot>
        </div>
      </template>
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
    label: String,
  },
  components: {
    VueApexCharts,
    DsfrAccordion,
  },
  mounted() {
    if (!this.heading && !this.label) {
      console.warn(
        `Graph ${this.graphId} should have an accessible title. Please set either the heading prop or the label prop.`
      )
    }
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
