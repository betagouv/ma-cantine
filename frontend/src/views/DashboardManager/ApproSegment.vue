<template>
  <div>
    <div v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic" class="body-1">
      <p class="font-weight-bold">Pilotez votre progression tout au long de l’année en cours</p>
      <p class="body-2">
        Avec l’outil de suivi d’achats de “ma cantine”, calculez automatiquement et en temps réel la part de vos
        approvisionnements qui correspondent aux critères de la loi EGAlim, et facilitez ainsi votre prochaine
        télédéclaration.
      </p>
      <p class="body-2">
        Pour cela, vous pouvez renseigner tous vos achats au fil de l’eau ou par import en masse, ou bien connecter
        votre outil de gestion habituel si cela est possible pour transférer les données.
      </p>
    </div>
  </div>
</template>
<script>
export default {
  name: "ApproSegment",
  props: {
    purchases: {
      type: Array,
    },
    currentDiagnostic: {
      type: Object,
    },
    lastYearDiagnostic: {
      type: Object,
    },
  },
  computed: {
    hasPurchases() {
      return false
    },
    hasCurrentDiagnostic() {
      return false
    },
    hasLastYearDiagnostic() {
      return false
    },
  },
}
</script>
