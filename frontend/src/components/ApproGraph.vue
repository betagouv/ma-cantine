<template>
  <VueApexCharts
    :options="chartOptions"
    :series="series"
    role="img"
    aria-description="Approvisionnement bio et durable"
    height="100px"
    width="100%"
    class="my-4"
  />
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import { applicableDiagnosticRules, getSustainableTotal, getPercentage } from "@/utils"

export default {
  name: "ApproGraph",
  components: { VueApexCharts },
  props: {
    diagnostic: {
      type: Object,
    },
    canteen: {
      type: Object,
    },
  },
  computed: {
    chartOptions() {
      return {
        chart: {
          animations: {
            enabled: false,
          },
          type: "bar",
          stacked: true,
          toolbar: { show: false },
        },
        tooltip: {
          enabled: false,
        },
        states: {
          hover: {
            filter: {
              type: "none",
            },
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        xaxis: {
          max: 100,
          min: 0,
          tickAmount: 4,
          labels: { show: false },
          axisTicks: { show: false },
        },
        yaxis: {
          labels: { show: false },
        },
        grid: {
          padding: {
            left: -14,
          },
        },
        dataLabels: {
          enabled: false,
        },
        annotations: {
          xaxis: [
            {
              x: this.applicableRules.qualityThreshold,
              borderColor: "#00A95F",
              label: {
                offsetY: -14,
                orientation: "horizontal",
                style: {
                  color: "#00A95F",
                  background: "#fff",
                },
                text: `${this.applicableRules.qualityThreshold} %`,
              },
            },
            {
              x: this.applicableRules.bioThreshold,
              borderColor: "#297254",
              label: {
                offsetY: -14,
                orientation: "horizontal",
                style: {
                  color: "#297254",
                  background: "#fff",
                },
                text: `${this.applicableRules.bioThreshold} %`,
              },
            },
          ],
        },
      }
    },
    series() {
      return [
        {
          name: `Bio : ${this.bioPercentage} %`,
          data: [this.bioPercentage],
          color: "#297254",
        },
        {
          name: `Durable et de qualité : ${this.sustainablePercentage} %`,
          data: [this.sustainablePercentage],
          color: "#00A95F",
        },
      ]
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    bioPercentage() {
      const percentage =
        Math.round(this.diagnostic.percentageValueBioHt * 100) ||
        getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt, true)
      return percentage || 0
    },
    sustainablePercentage() {
      return "percentageValueTotalHt" in this.diagnostic
        ? Math.round(getSustainableTotal(this.diagnostic) * 100)
        : getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt)
    },
  },
}
</script>
