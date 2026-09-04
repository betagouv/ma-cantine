<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="displayDiversificationPlanSegment">
        <span v-if="diagnostic.hasDiversificationPlan">
          <v-icon color="primary" class="mr-1">$check-line</v-icon>
          <span>
            {{ constantsDiversificationMeasureStep.hasDiversificationPlan.title }}
            <ul role="list" class="mt-2" v-if="appliedDiversificationActions && appliedDiversificationActions.length">
              <li class="fr-text-xs mb-1" v-for="action in appliedDiversificationActions" :key="action">
                {{ action }}
              </li>
            </ul>
            <ul role="list" class="mt-2" v-else>
              <li class="fr-text-xs mb-1">
                {{ constantsDiversificationMeasureStep.diversificationPlanActions.empty }}
              </li>
            </ul>
          </span>
        </span>
        <span v-else-if="diagnosticUsesNullAsFalse || diagnostic.hasDiversificationPlan === false">
          <v-icon color="primary" class="mr-1">$close-line</v-icon>
          <span>
            {{ constantsDiversificationMeasureStep.hasDiversificationPlan.false }}
          </span>
        </span>
        <span v-else>
          <v-icon color="primary" class="mr-1">$question-line</v-icon>
          <span>
            {{ constantsDiversificationMeasureStep.hasDiversificationPlan.empty }}
          </span>
        </span>
      </li>

      <li v-if="diagnostic.serviceType">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          {{ constantsDiversificationMeasureStep.serviceType.title }}
          <span class="font-weight-bold">{{ serviceType }}</span>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          {{ constantsDiversificationMeasureStep.serviceType.empty }}
        </div>
      </li>

      <li v-if="diagnostic.vegetarianWeeklyRecurrence">
        <v-icon v-if="diagnostic.vegetarianWeeklyRecurrence === 'NEVER'" color="primary" class="mr-2">
          $close-line
        </v-icon>
        <v-icon v-else color="primary" class="mr-2">$check-line</v-icon>
        <div>
          {{ constantsDiversificationMeasureStep.vegetarianWeeklyRecurrence.title }}
          <span class="font-weight-bold">{{ vegetarianWeeklyRecurrence }}</span>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          {{ constantsDiversificationMeasureStep.vegetarianWeeklyRecurrence.empty }}
        </div>
      </li>

      <!--TODO : remove year check when we stop displaying diagnostic summary for previous years -->
      <div v-if="diagnostic.vegetarianWeeklyRecurrence !== 'NEVER' && diagnostic.year < 2025">
        <li v-if="diagnostic.vegetarianMenuType">
          <v-icon color="primary" class="mr-2">$check-line</v-icon>
          <div>
            {{ constantsDiversificationMeasureStep.vegetarianMenuType.title }}
            <span class="font-weight-bold">{{ vegetarianMenuType }}</span>
          </div>
        </li>
        <li v-else>
          <v-icon color="primary" class="mr-2">$question-line</v-icon>
          <div>
            {{ constantsDiversificationMeasureStep.vegetarianMenuType.empty }}
          </div>
        </li>
      </div>

      <div v-if="diagnostic.vegetarianWeeklyRecurrence !== 'NEVER'">
        <li v-if="diagnostic.vegetarianMenuBases && diagnostic.vegetarianMenuBases.length">
          <v-icon color="primary" class="mr-2">$check-line</v-icon>
          <div>
            {{ constantsDiversificationMeasureStep.vegetarianMenuBases.title }}
            <ul role="list" class="mt-2" v-if="vegetarianMenuBases && vegetarianMenuBases.length">
              <li class="fr-text-xs mb-1" v-for="base in vegetarianMenuBases" :key="base">
                {{ base }}
              </li>
            </ul>
          </div>
        </li>
        <li v-else>
          <v-icon color="primary" class="mr-2">$question-line</v-icon>
          <div>
            {{ constantsDiversificationMeasureStep.vegetarianMenuBases.empty }}
          </div>
        </li>
      </div>
    </ul>
  </div>
</template>

<script>
import { applicableDiagnosticRules, selectListToObject, diagnosticUsesNullAsFalse } from "@/utils"
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
  data() {
    return {
      constantsDiversificationMeasureStep: Constants.DiversificationMeasureStep,
    }
  },
  computed: {
    serviceType() {
      const items = selectListToObject(this.constantsDiversificationMeasureStep.serviceType.items)
      return items[this.diagnostic.serviceType]
    },
    vegetarianWeeklyRecurrence() {
      const items = selectListToObject(this.constantsDiversificationMeasureStep.vegetarianWeeklyRecurrence.items)
      return items[this.diagnostic.vegetarianWeeklyRecurrence]
    },
    vegetarianMenuType() {
      const items = selectListToObject(this.constantsDiversificationMeasureStep.vegetarianMenuType.items)
      return items[this.diagnostic.vegetarianMenuType]
    },
    vegetarianMenuBases() {
      const items = selectListToObject(this.constantsDiversificationMeasureStep.vegetarianMenuBases.items)
      return this.diagnostic.vegetarianMenuBases.map((x) => items[x])
    },
    displayDiversificationPlanSegment() {
      return applicableDiagnosticRules(this.canteen).hasDiversificationPlan
    },
    appliedDiversificationActions() {
      const diversificationPlanActions = selectListToObject(
        this.constantsDiversificationMeasureStep.diversificationPlanActions.items
      )
      if (!this.diagnostic.diversificationPlanActions?.length) return null
      return this.diagnostic.diversificationPlanActions.map((x) => diversificationPlanActions[x]).filter((x) => !!x)
    },
    diagnosticUsesNullAsFalse() {
      return diagnosticUsesNullAsFalse(this.diagnostic)
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
