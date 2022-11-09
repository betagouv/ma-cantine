<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" />
    <h1 class="font-weight-black text-h4 mb-2">Actions en attente</h1>
    <p class="mt-0 mb-8">Concernent la télédéclaration pour l'année {{ year }}</p>
    <AnnualActionableCanteensTable />
  </div>
</template>

<script>
import AnnualActionableCanteensTable from "./AnnualActionableCanteensTable"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "PendingActions",
  components: { AnnualActionableCanteensTable, BreadcrumbsNav },
  data() {
    return {
      year: 2021,
    }
  },
}
</script>
