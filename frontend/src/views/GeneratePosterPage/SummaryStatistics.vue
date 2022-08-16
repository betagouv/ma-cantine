<template>
  <div>
    <VueApexCharts
      :width="width || ($vuetify.breakpoint.smAndDown ? 280 : 320)"
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
import { getSustainableTotal } from "@/utils"
import VueApexCharts from "vue-apexcharts"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    qualityDiagnostic: Object,
    width: Number,
    hideLegend: Boolean,
  },
  computed: {
    dataPresent() {
      return !!this.qualityDiagnostic.valueTotalHt
    },
    bioPercentage() {
      return getPercentage(this.qualityDiagnostic.valueBioHt, this.qualityDiagnostic.valueTotalHt)
    },
    sustainablePercentage() {
      return getPercentage(getSustainableTotal(this.qualityDiagnostic), this.qualityDiagnostic.valueTotalHt)
    },
    series() {
      return [this.bioPercentage, this.sustainablePercentage, 100 - this.bioPercentage - this.sustainablePercentage]
    },
    chartOptions() {
      return {
        plotOptions: {
          pie: {
            expandOnClick: false,
          },
        },
        chart: {
          type: "pie",
          animations: {
            enabled: false,
          },
        },
        tooltip: {
          enabled: false,
        },
        states: {
          active: {
            filter: {
              type: "none",
            },
          },
          hover: {
            filter: {
              type: "none",
            },
          },
        },
        labels: ["Bio", "Qualité et durable (hors bio)", "Hors catégories EGAlim"],
        colors: ["#297254", "#00A95F", "#ccc"],
        legend: {
          show: !this.hideLegend,
          fontSize: "12px",
          position: "right",
        },
        dataLabels: {
          formatter(value) {
            return value + "%"
          },
          dropShadow: {
            enabled: false,
          },
        },
      }
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
