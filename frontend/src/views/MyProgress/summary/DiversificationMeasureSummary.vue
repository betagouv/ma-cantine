<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="displayDiversificationPlanSegment && displayDiagnostic.hasDiversificationPlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de
          protéines végétales
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="action in appliedDiversificationActions" :key="action">
              {{ action }}
            </li>
          </ul>
        </div>
      </li>
      <li v-else-if="displayDiversificationPlanSegment">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base
          de protéines végétales
        </div>
      </li>

      <li v-if="displayDiagnostic.vegetarianWeeklyRecurrence">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai mis en place un menu végétarien dans ma cantine :
          <span class="font-weight-bold">{{ weeklyRecurrence }}</span>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas renseigné la périodicité du menu végétarien dans ma cantine
        </div>
      </li>

      <li v-if="displayDiagnostic.vegetarianMenuType">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Le menu végétarien proposé est :
          <span class="font-weight-bold">{{ menuType }}</span>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas renseigné le type de menu végétarien servi dans ma cantine
        </div>
      </li>

      <li v-if="displayDiagnostic.vegetarianMenuBases && displayDiagnostic.vegetarianMenuBases.length">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Le plat principal de mon menu végétarien est majoritairement à base de :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="base in menuBases" :key="base">
              {{ base }}
            </li>
          </ul>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas renseigné les bases utilisées pour mon menu végétarien
        </div>
      </li>

      <li v-if="canteen.vegetarianExpeParticipant">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je suis volontaire pour l’expérimentation de l’option végétarienne quotidienne
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je ne suis pas volontaire pour l’expérimentation de l’option végétarienne quotidienne
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"

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
    displayDiversificationPlanSegment() {
      return applicableDiagnosticRules(this.canteen).hasDiversificationPlan
    },
    appliedDiversificationActions() {
      const diversificationPlanActions = {
        PRODUCTS:
          "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
        PRESENTATION: "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
        MENU: "Agir sur la manière dont les menus sont conçus en soulignant attributs positifs des plats",
        PROMOTION: "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
        TRAINING:
          "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
      }
      if (!this.displayDiagnostic.diversificationPlanActions?.length) return null
      return this.displayDiagnostic.diversificationPlanActions
        .map((x) => diversificationPlanActions[x])
        .filter((x) => !!x)
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
  display: flex;
}
li .v-icon {
  align-items: baseline;
}
</style>
