<template>
  <div>
    <VueApexCharts
      :width="$vuetify.breakpoint.smAndDown ? 280 : 350"
      :options="chartOptions"
      :series="series"
      v-if="dataPresent"
      role="img"
      :aria-label="series[0] + ' % produits bio, ' + series[1] + ' % produits de qualité et durables'"
    />
    <div class="no-data" v-if="!dataPresent">Données non renseignées</div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    qualityDiagnostic: Object,
  },
  data() {
    return {
      chartOptions: {
        chart: {
          type: "pie",
        },
        labels: ["Bio", "Qualité et durable (hors bio)", "Hors EGAlim"],
        colors: ["#61753f", "#EB5B25", "#E2A013"],
        legend: {
          fontSize: "12px",
          position: "top",
        },
        dataLabels: {
          formatter: function(value) {
            return value + "%"
          },
          dropShadow: {
            enabled: false,
          },
        },
      },
    }
  },
  computed: {
    dataPresent() {
      return (
        !!this.qualityDiagnostic.valueTotalHt &&
        (!!this.qualityDiagnostic.valueBioHt || !!this.qualityDiagnostic.valueSustainableHt)
      )
    },
    bioPercentage() {
      return getPercentage(this.qualityDiagnostic.valueBioHt, this.qualityDiagnostic.valueTotalHt)
    },
    sustainablePercentage() {
      return getPercentage(this.qualityDiagnostic.valueSustainableHt, this.qualityDiagnostic.valueTotalHt)
    },
    series() {
      return [this.bioPercentage, this.sustainablePercentage, 100 - this.bioPercentage - this.sustainablePercentage]
    },
  },
}

function getPercentage(partialValue, totalValue) {
  return !!partialValue && !!totalValue ? Math.round((100 * partialValue) / totalValue) : 0
}
</script>

<style scoped lang="scss">
.no-data {
  text-align: center;
  line-height: 200px;
  font-style: italic;
}

@media (max-width: 930px) {
  .no-data {
    line-height: 150px;
  }
}

@media (max-width: 420px) {
  .no-data {
    line-height: 100px;
  }
}
</style>
