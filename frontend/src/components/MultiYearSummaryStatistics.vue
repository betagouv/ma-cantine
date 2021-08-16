<template>
  <div>
    <VueApexCharts
      :options="chartOptions"
      :series="series"
      role="img"
      :aria-labelledby="headingId"
      aria-describedby="text"
    />
    <p id="text" class="d-none">{{ description }}</p>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"

const VALUE_DESCRIPTION = "Pourcentage du total d'achats alimentaires (en HT)"
const NO_DATA = "Données non renseignées"
const BIO = "Bio"
const SUSTAINABLE = "Qualité et durable (hors bio)"
const OTHER = "Hors EGAlim"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    diagnostics: Object,
    headingId: String,
  },
  data() {
    const diagArray = Object.values(this.diagnostics)
    const years = diagArray.map((d) => d.year)
    return {
      years,
      chartOptions: {
        chart: {
          type: "bar",
          stacked: true,
          toolbar: { tools: { download: false } },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        xaxis: {
          categories: years,
          labels: {
            formatter: percentageFormatter,
          },
          title: {
            text: VALUE_DESCRIPTION,
          },
        },
        yaxis: {
          title: {
            text: "Année",
          },
          max: 100,
        },
        annotations: {
          xaxis: [
            {
              x: 50,
              borderColor: "#333",
              label: {
                borderColor: "#333",
                style: {
                  color: "#fff",
                  background: "#333",
                },
                text: "Objectif EGAlim 2022",
              },
            },
          ],
        },
        tooltip: {
          y: {
            formatter: percentageFormatter,
          },
        },
        fill: {
          opacity: 1,
        },
        legend: {
          position: "top",
          horizontalAlign: "left",
          offsetX: 40,
        },
      },
    }
  },
  computed: {
    seriesData() {
      const diagArray = Object.values(this.diagnostics)
      diagArray.forEach((d) => {
        if (myIsNaN(d.valueBioHt) || myIsNaN(d.valueSustainableHt) || myIsNaN(d.valueTotalHt)) {
          d.incompleteValues = true
        }
      })
      return {
        bio: diagArray.map((d) => getPercentage(d.valueBioHt, d.valueTotalHt)),
        sustainable: diagArray.map((d) => getPercentage(d.valueSustainableHt, d.valueTotalHt)),
        other: diagArray.map((d) => {
          if (d.incompleteValues) {
            return undefined
          } else {
            return (
              100 - getPercentage(d.valueBioHt, d.valueTotalHt) - getPercentage(d.valueSustainableHt, d.valueTotalHt)
            )
          }
        }),
        incompleteValues: diagArray.map((d) => d.incompleteValues),
      }
    },
    series() {
      return [
        {
          name: BIO,
          data: this.seriesData.bio,
          color: "#0c7f46",
        },
        {
          name: SUSTAINABLE,
          data: this.seriesData.sustainable,
          color: "#ff8d7e",
        },
        {
          name: OTHER,
          data: this.seriesData.other,
          color: "#7F7FC8",
        },
      ]
    },
    description() {
      let description = `${VALUE_DESCRIPTION}. `
      this.years.forEach((year, idx) => {
        description += `${year} : `
        if (this.seriesData.incompleteValues[idx]) {
          description += `${NO_DATA}. `
        } else {
          description += `${percentageFormatter(this.seriesData.bio[idx])} ${BIO}, ${percentageFormatter(
            this.seriesData.sustainable[idx]
          )} ${SUSTAINABLE}. `
        }
      })
      return description
    },
  },
}

function getPercentage(partialValue, totalValue) {
  if (myIsNaN(partialValue) || myIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return Math.round((100 * partialValue) / totalValue)
  }
}

function myIsNaN(x) {
  return Number(x) !== x
}

function percentageFormatter(val) {
  return val + " %"
}
</script>
