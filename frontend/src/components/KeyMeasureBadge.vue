<template>
  <DsfrBadge v-if="tab.isCompleted" :showIcon="false" mode="SUCCESS">Complété</DsfrBadge>
  <DsfrBadge v-else-if="tab.isRequired" :showIcon="false" mode="ERROR">À compléter (obligatoire)</DsfrBadge>
  <DsfrBadge v-else :showIcon="false" mode="WARNING">À compléter (optionnel)</DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"

// TODO =
// 1 état rouge bloque la TD : à compléter
// 1 état jaune : à compléter (optionnel)
// 1 état gris / appro + SAT seulement :  à compléter (par livreur des repas)
// 2 états vert : complété solo || TD par livreur des repas
export default {
  props: {
    tab: Object,
  },
  components: {
    DsfrBadge,
  },
}
</script>
