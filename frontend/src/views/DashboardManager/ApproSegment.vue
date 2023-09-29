<template>
  <div class="fill-height">
    <div v-if="showFirstTimeView" class="body-1">
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
    <div v-else-if="!hasApproData">
      TODO : Page 3000
    </div>
    <v-card outlined class="fill-height d-flex flex-column dsfr" v-else-if="diagnostic">
      <v-card-title class="font-weight-bold body-1">
        <v-icon color="red" class="mr-2">
          mdi-food-apple
        </v-icon>
        <span>Qualité des produits</span>
      </v-card-title>
      <v-card-text :class="`mt-n4 pl-12 py-0 ${level.colorClass}`">
        NIVEAU :
        <span class="font-weight-bold">{{ level.text }}</span>
      </v-card-text>
      <v-card-text>
        <VueApexCharts
          :options="chartOptions"
          :series="series"
          role="img"
          aria-description="Approvisionnement bio et durable"
          height="100px"
          width="100%"
          class="my-4"
        />
        <p class="body-2">
          C’est parti ! Découvrez les outils et les ressources personnalisées pour vous aider à atteindre un des deux
          objectifs EGAlim et passer au niveau suivant !
        </p>
      </v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions class="px-4 pt-0">
        <v-spacer></v-spacer>
        <v-icon color="primary">$arrow-right-line</v-icon>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { hasDiagnosticApproData, getSustainableTotal, getPercentage, applicableDiagnosticRules } from "@/utils"
import VueApexCharts from "vue-apexcharts"
import Constants from "@/constants"

export default {
  name: "ApproSegment",
  components: { VueApexCharts },
  props: {
    purchases: {
      type: Array,
    },
    diagnostic: {
      type: Object,
    },
    lastYearDiagnostic: {
      type: Object,
    },
  },
  computed: {
    hasApproData() {
      return this.diagnostic && hasDiagnosticApproData(this.diagnostic)
    },
    level() {
      return Constants.Levels.BEGINNER
    },
    showFirstTimeView() {
      return !this.hasPurchases && !this.diagnostic && !this.hasLastYearDiagnostic
    },
    hasPurchases() {
      return false
    },
    hasLastYearDiagnostic() {
      return false
    },
    bioPercentage() {
      return getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt, true)
    },
    sustainablePercentage() {
      return getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt, true)
    },
    chartOptions() {
      return {
        chart: {
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
  },
}
</script>
