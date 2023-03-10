<template>
  <div>
    <VueApexCharts
      :options="chartOptions"
      :series="series"
      role="img"
      aria-description="Répartition par famille de produit"
      :height="this.height || 'auto'"
      :width="this.width || '100%'"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import Constants from "@/constants"
import colors from "vuetify/lib/util/colors"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    diagnostic: Object,
    height: String,
    width: String,
  },
  data() {
    const families = Object.keys(Constants.ProductFamilies).map((f) => ({
      id: f,
      ...Constants.ProductFamilies[f],
    }))
    const familiesLabels = families.map((f) => f.text)
    const characteristics = Constants.TeledeclarationCharacteristicGroups.egalim.characteristics.map((c) => ({
      id: c,
      ...Constants.TeledeclarationCharacteristics[c],
    }))
    return {
      families,
      familiesLabels,
      characteristics,
    }
  },
  computed: {
    seriesData() {
      const seriesData = {}
      for (let i = 0; i < this.characteristics.length; i++) {
        const characteristic = this.characteristics[i]
        seriesData[characteristic.id] = this.getValuesForCharacteristic(characteristic.id)
      }
      return seriesData
    },
    series() {
      return this.characteristics.map((x) => ({
        name: x.text,
        data: this.seriesData[x.id],
        color: this.getHexColor(x.color),
      }))
    },
    chartOptions() {
      const maxLine = this.$vuetify.breakpoint.mdAndUp ? 25 : 20
      const legendPosition = this.$vuetify.breakpoint.mdAndUp ? "right" : "top"
      const legendAlign = this.$vuetify.breakpoint.mdAndUp ? "left" : "center"
      return {
        chart: {
          type: "bar",
          stacked: true,
          stackType: "100%",
          toolbar: { tools: { download: false } },
          animations: {
            enabled: false,
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        states: {
          hover: {
            filter: {
              type: "darken",
              value: 0.75,
            },
          },
        },
        xaxis: {
          categories: this.familiesLabels.map((x) => this.getPhrases(x, maxLine)),
          labels: {
            formatter: percentageFormatter,
          },
          max: 100,
          min: 0,
          tickAmount: 4,
        },
        legend: {
          position: legendPosition,
          horizontalAlign: legendAlign,
        },
        dataLabels: {
          enabled: true,
          formatter: roundFormatter,
          style: {
            fontSize: "10px",
          },
        },
        tooltip: {
          y: {
            formatter: function(value, { series, seriesIndex }) {
              const row = series[seriesIndex]
              const sum = row.reduce((a, b) => a + b, 0)
              const percentage = (value / sum) * 100
              return `${percentage.toFixed(2)} %`
            },
          },
        },
      }
    },
  },
  methods: {
    getPhrases(text, lineLength) {
      /*
      Because of this issue :https://github.com/apexcharts/apexcharts.js/issues/640
      we need to split the y-axis categories so they appear multi-line.
      Has a limitation with individual words that are longer than the line-length, but
      we don't have that case currently.
      */
      const words = text.split(" ")
      const phrases = []
      for (let i = 0; i < words.length; i++) {
        const word = words[i]
        if (phrases.length === 0) {
          phrases.push(word)
          continue
        }
        const currentPhrase = phrases[phrases.length - 1]
        if (currentPhrase.length + word.length + 1 < lineLength) {
          phrases[phrases.length - 1] = `${currentPhrase} ${word}`
        } else {
          phrases.push(word)
        }
      }
      return phrases
    },
    getHexColor(vuetifyColor) {
      const elements = vuetifyColor.split(" ")
      const baseColor = elements[0]
      const modifier = elements.length === 2 ? elements[1].replace("-", "") : "base"
      return colors[baseColor][modifier]
    },
    getValuesForCharacteristic(characteristicId) {
      const baseFields = {
        VIANDES_VOLAILLES: "valueViandesVolailles",
        CHARCUTERIE: "valueCharcuterie",
        PRODUITS_DE_LA_MER: "valueProduitsDeLaMer",
        FRUITS_ET_LEGUMES: "valueFruitsEtLegumes",
        PRODUITS_LAITIERS: "valueProduitsLaitiers",
        BOULANGERIE: "valueBoulangerie",
        BOISSONS: "valueBoissons",
        AUTRES: "valueAutres",
      }
      const baseModifiers = {
        BIO: "Bio",
        LABEL_ROUGE: "LabelRouge",
        AOCAOP_IGP_STG: "AocaopIgpStg",
        HVE: "Hve",
        PECHE_DURABLE: "PecheDurable",
        RUP: "Rup",
        COMMERCE_EQUITABLE: "CommerceEquitable",
        FERMIER: "Fermier",
        EXTERNALITES: "Externalites",
        PERFORMANCE: "Performance",
      }
      const modifier = baseModifiers[characteristicId]
      const diag = this.diagnostic
      return this.families.map((family) => {
        const baseField = baseFields[family.id]
        const field = `${baseField}${modifier}`
        return diag[field]
      })
    },
  },
}

function percentageFormatter(val) {
  return val + " %"
}
function roundFormatter(val) {
  return Math.round(val)
}
</script>
