<template>
  <div class="fr-text">
    <ul>
      <li v-if="displayDiagnostic.vegetarianWeeklyRecurrence">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        J’ai mis en place un menu végétarien dans ma cantine :
        <span class="font-weight-bold">{{ weeklyRecurrence }}</span>
      </li>
      <li v-else>
        <v-icon color="grey darken-1" class="mr-2">$information-line</v-icon>
        Je n'ai pas renseigné la périodicité du menu végétarien dans ma cantine
      </li>

      <li v-if="displayDiagnostic.vegetarianMenuType">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Le menu végétarien proposé est :
        <span class="font-weight-bold">{{ menuType }}</span>
      </li>
      <li v-else>
        <v-icon color="grey darken-1" class="mr-2">$information-line</v-icon>
        Je n'ai pas renseigné le type de menu végétarien servi dans ma cantine
      </li>

      <li v-if="displayDiagnostic.vegetarianMenuBases && displayDiagnostic.vegetarianMenuBases.length">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Le plat principal de mon menu végétarien est majoritairement à base de :
        <ul class="mt-2">
          <li class="fr-text-xs ml-9 mb-1" v-for="base in menuBases" :key="base">
            {{ base }}
          </li>
        </ul>
      </li>

      <li v-if="canteen.vegetarianExpeParticipant">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je suis volontaire pour l’expérimentation de l’option végétarienne quotidienne
      </li>
      <li v-else>
        <v-icon color="grey darken-1" class="mr-2">$information-line</v-icon>
        Je ne suis pas volontaire pour l’expérimentation de l’option végétarienne quotidienne
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "DiversificationMeasureSummary",
  props: {
    diagnostic: {},
    centralDiagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
    },
    weeklyRecurrence() {
      return {
        LOW: "Moins d'une fois par semaine",
        MID: "Une fois par semaine",
        HIGH: "Plus d'une fois par semaine",
        DAILY: "De façon quotidienne",
      }[this.displayDiagnostic.vegetarianWeeklyRecurrence]
    },
    menuType() {
      return {
        UNIQUE: "Un menu végétarien en plat unique, sans choix",
        SEVERAL: "Un menu végétarien composé de plusieurs choix de plats végétariens",
        ALTERNATIVES: "Un menu végétarien au choix, en plus d'autres plats non végétariens",
      }[this.displayDiagnostic.vegetarianMenuType]
    },
    menuBases() {
      const bases = {
        GRAIN: "De céréales et/ou les légumes secs (hors soja)",
        SOY: "De soja",
        CHEESE: "De fromage",
        EGG: "D’œufs",
        READYMADE: "Plats prêts à l'emploi",
      }
      return this.displayDiagnostic.vegetarianMenuBases.map((x) => bases[x])
    },
  },
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 14px;
}
</style>
