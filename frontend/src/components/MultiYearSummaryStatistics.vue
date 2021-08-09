<template>
  <!-- TODO: better alt text and tabbable download button -->
  <VueApexCharts :options="chartOptions" :series="series" role="img" />
</template>

<script>
import VueApexCharts from "vue-apexcharts"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    diagnostics: Object,
  },
  data() {
    const diagArray = Object.values(this.diagnostics)
    diagArray.forEach((d) => {
      if (myIsNaN(d.valueBioHt) || myIsNaN(d.valueSustainableHt) || myIsNaN(d.valueTotalHt)) {
        d.valuesIncomplete = true
      }
    })
    return {
      series: [
        {
          name: "Bio",
          data: diagArray.map((d) => getPercentage(d.valueBioHt, d.valueTotalHt)),
          color: "#0c7f46",
        },
        {
          name: "Qualité et durable (hors bio)",
          data: diagArray.map((d) => getPercentage(d.valueSustainableHt, d.valueTotalHt)),
          color: "#ff8d7e",
        },
        {
          name: "Hors EGAlim",
          data: diagArray.map((d) => {
            if (d.valuesIncomplete) {
              return undefined
            } else {
              return (
                100 - getPercentage(d.valueBioHt, d.valueTotalHt) - getPercentage(d.valueSustainableHt, d.valueTotalHt)
              )
            }
          }),
          color: "#7F7FC8",
        },
      ],
      // TODO: explore whether to make this work
      // noData: {
      //   text: "Données pas disponibles",
      //   align: "center",
      //   verticalAlign: "middle",
      //   offsetX: 100,
      //   offsetY: 0,
      //   style: {
      //     color: "#333",
      //     fontSize: "14px",
      //     fontFamily: "Marianne",
      //   },
      // },
      chartOptions: {
        chart: {
          type: "bar",
          stacked: true,
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        xaxis: {
          // TODO: how to do this dynamically? last four years and none for no data?
          // TODO: note that 2021, 2022 is provisional?
          categories: [2019, 2020, 2021, 2022],
          labels: {
            formatter: percentageFormatter,
          },
          title: {
            text: "Pourcentage de valeur total d'achats alimentaires (en HT)",
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
                text: "Atteint EGAlim 2022",
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
