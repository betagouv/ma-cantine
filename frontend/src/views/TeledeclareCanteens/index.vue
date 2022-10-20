<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" />
    <h1 class="font-weight-black text-h4 mb-4">Télédéclarer mes cantines pour {{ year }}</h1>
    <AnnualCanteenSummaryTable />
  </div>
</template>

<script>
import AnnualCanteenSummaryTable from "./AnnualCanteenSummaryTable"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "TeledeclareCanteens",
  components: { AnnualCanteenSummaryTable, BreadcrumbsNav },
  data() {
    return {
      year: 2021,
    }
  },
}
</script>
