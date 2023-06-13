<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" />
    <h1 class="font-weight-black text-h4 mb-8">Actions en attente en {{ year }}</h1>
    <AnnualActionableCanteensTable />
  </div>
</template>

<script>
import AnnualActionableCanteensTable from "./AnnualActionableCanteensTable"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import { lastYear } from "@/utils"

export default {
  name: "PendingActions",
  components: { AnnualActionableCanteensTable, BreadcrumbsNav },
  data() {
    return {
      year: lastYear(),
    }
  },
}
</script>
