<template>
  <div>
    <p v-if="!hasEnoughData && fallbackText">{{ fallbackText }}</p>
    <VueApexCharts
      v-else
      :options="chartOptions"
      :series="series"
      role="figure"
      aria-label="Approvisionnement bio et durable"
      :aria-description="description"
      height="100px"
      width="100%"
      class="my-4"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import { applicableDiagnosticRules, getSustainableTotal, getPercentage, hasApproGraphData } from "@/utils"

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
    colorTheme: {
      type: String,
      optional: true,
    },
    fallbackText: {
      type: String,
      optional: true,
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
              borderColor: this.theme.sustainable,
              label: {
                offsetY: -14,
                orientation: "horizontal",
                style: {
                  color: this.theme.sustainable,
                  background: "#fff",
                },
                text: `${this.applicableRules.qualityThreshold} %`,
              },
            },
            {
              x: this.applicableRules.bioThreshold,
              borderColor: this.theme.bio,
              label: {
                offsetY: -14,
                orientation: "horizontal",
                style: {
                  color: this.theme.bio,
                  background: "#fff",
                },
                text: `${this.applicableRules.bioThreshold} %`,
              },
            },
          ],
        },
      }
    },
    theme() {
      const themes = {
        green: {
          bio: "#21402c",
          sustainable: "#00A95F",
        },
        blue: {
          bio: "#263b58", // blue-cumulus-200
          sustainable: "#5982E0",
        },
        brown: {
          bio: "#543125", // orange-terre-battue-200
          sustainable: "#AB7B6B",
        },
      }
      if (this.colorTheme) return themes[this.colorTheme]
      if (this.diagnostic.isTeledeclared) return themes.green
      else if (this.diagnostic.year >= new Date().getFullYear()) return themes.blue
      return themes.brown
    },
    series() {
      return [
        {
          name: `Bio : ${this.bioPercentage} %`,
          data: [this.bioPercentage],
          color: this.theme.bio,
        },
        {
          name: `Durable et de qualité : ${this.sustainablePercentage} %`,
          data: [this.sustainablePercentage],
          color: this.theme.sustainable,
        },
      ]
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    bioPercentage() {
      const percentage =
        this.diagnostic.percentageValeurBio >= 0
          ? Math.round(this.diagnostic.percentageValeurBio * 100)
          : getPercentage(this.diagnostic.valeurBio, this.diagnostic.valeurTotale, true)
      return this.isTruthyOrZero(percentage) ? percentage : "—"
    },
    sustainablePercentage() {
      const percentage =
        "percentageValeurTotale" in this.diagnostic
          ? Math.round(getSustainableTotal(this.diagnostic) * 100)
          : getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valeurTotale)
      return this.isTruthyOrZero(percentage) ? percentage : "—"
    },
    description() {
      return `Bio : ${this.bioPercentage} %. Durable et de qualité (hors bio) : ${this.sustainablePercentage} %. Rappel objectif EGalim : ${this.applicableRules.qualityThreshold} % des achats de qualité et durable, dont ${this.applicableRules.bioThreshold} % bio.`
    },
    hasEnoughData() {
      return hasApproGraphData(this.diagnostic)
    },
  },
  methods: {
    isTruthyOrZero(value) {
      return !!value || value === 0
    },
  },
}
</script>
