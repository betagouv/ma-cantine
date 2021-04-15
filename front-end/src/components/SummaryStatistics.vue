<template>
  <div>
    <VueApexCharts
      width="400"
      :options="chartOptions"
      :series="series"
      v-if="dataPresent"
      role="img"
      :aria-label="series[0] +' % produits bio, ' + series[1] + ' % produits de qualité et durables'"
    />
    <div class="no-data" v-else>Données non renseignées</div>
  </div>
</template>

<script>
  import VueApexCharts from "vue3-apexcharts";

  export default {
    el: '#appl',
    components: {
      VueApexCharts,
    },
    props: {
      qualityDiagnostic: Object,
    },
    data() {
      const bioPercentage = getPercentage(this.qualityDiagnostic.valueBio, this.qualityDiagnostic.valueTotal);
      const sustainablePercentage = getPercentage(this.qualityDiagnostic.valueSustainable, this.qualityDiagnostic.valueTotal);

      return {
        dataPresent: !!this.qualityDiagnostic.valueTotal && (!!this.qualityDiagnostic.valueBio || !!this.qualityDiagnostic.valueSustainable),
        series: [
          bioPercentage,
          sustainablePercentage,
          100 - bioPercentage - sustainablePercentage
        ],
        chartOptions: {
          chart: {
            type: 'pie',
          },
          labels: ['Bio', 'Qualité et durable', 'Hors EGAlim'],
          colors: ['#61753f', '#EB5B25', '#E2A013'],
          legend: {
            fontSize: '16px',
          },
          dataLabels: {
            formatter: function (value) {
              return value + "%";
            },
            dropShadow: {
              enabled: false,
            },
          },
          responsive: [{
            breakpoint: 930,
            options: {
              chart: {
                width: 350
              },
            }
          },
          {
            breakpoint: 420,
            options: {
              chart: {
                width: 300
              },
              legend: {
                fontSize: '12px',
              },
            }
          }]
        },
      }
    }
  }

  function getPercentage(partialValue, totalValue) {
    return !!partialValue && !!totalValue ? Math.round((100 * partialValue) / totalValue) : '--';
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
