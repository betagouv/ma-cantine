<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.vegetarianWeeklyRecurrence">
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

      <li v-if="diagnostic.vegetarianMenuType">
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

      <li v-if="diagnostic.vegetarianMenuBases && diagnostic.vegetarianMenuBases.length">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Le plat principal de mon menu végétarien est majoritairement à base de :
          <ul role="list" class="mt-2" v-if="menuBases && menuBases.length">
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

      <li v-if="displayDiversificationPlanSegment && diagnostic.hasDiversificationPlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de
          protéines végétales
          <ul role="list" class="mt-2" v-if="appliedDiversificationActions && appliedDiversificationActions.length">
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
    </ul>
  </div>
</template>

<script>
import { applicableDiagnosticRules, selectListToObject } from "@/utils"
import Constants from "@/constants"

export default {
  name: "DiversificationMeasureSummary",
  props: {
    diagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    weeklyRecurrence() {
      const items = selectListToObject(Constants.VegetarianRecurrence)
      return items[this.diagnostic.vegetarianWeeklyRecurrence]
    },
    menuType() {
      const types = selectListToObject(Constants.VegetarianMenuTypes)
      return types[this.diagnostic.vegetarianMenuType]
    },
    menuBases() {
      const bases = selectListToObject(Constants.VegetarianMenuBases)
      return this.diagnostic.vegetarianMenuBases.map((x) => bases[x])
    },
    displayDiversificationPlanSegment() {
      return applicableDiagnosticRules(this.canteen).hasDiversificationPlan
    },
    appliedDiversificationActions() {
      const diversificationPlanActions = selectListToObject(Constants.DiversificationPlanActions)
      if (!this.diagnostic.diversificationPlanActions?.length) return null
      return this.diagnostic.diversificationPlanActions.map((x) => diversificationPlanActions[x]).filter((x) => !!x)
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
