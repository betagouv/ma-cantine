<script setup>
import { computed } from "vue"
import stringsService from "@/services/strings"
const props = defineProps(["stat", "objective", "label", "color"])

const gaugeColor = computed(() => props.color || "var(--green-emeraude-main-632)")
const hasObjective = computed(() => props.objective !== null && props.objective !== undefined)
const hasHatch = computed(() => hasObjective.value && props.stat < props.objective)
</script>

<template>
  <div class="graph-gauge fr-mb-3w">
    <p v-if="label" class="graph-gauge__label fr-mb-1w ma-cantine--bold">{{ label }}</p>
    <div class="graph-gauge__track">
      <div class="graph-gauge__progress" :style="`width: ${stat}%`"></div>
      <div
        v-if="hasHatch"
        class="graph-gauge__hatch"
        :style="`left: ${stat}%; width: ${objective - stat}%`"
      ></div>
      <div v-if="hasObjective" class="graph-gauge__objective" :style="`left: ${objective}%`"></div>
      <p
        class="graph-gauge__stat fr-mb-0 ma-cantine--bold fr-text--sm fr-px-1v"
        :style="`left: ${stat}%`"
      >
        {{ stringsService.prettyPercent(stat) }}
      </p>
    </div>
  </div>
</template>

<style lang="scss">
$graphHeight: 2.5rem;
$objectifColor: var(--text-mention-grey);
$hatchColor: var(--border-default-grey);

.graph-gauge {
  &__track {
    position: relative;
    height: $graphHeight;
    background-color: var(--background-contrast-grey);
  }

  &__progress,
  &__hatch {
    position: absolute;
    top: 0;
    bottom: 0;
  }

  &__progress {
    left: 0;
    background-color: v-bind(gaugeColor);
  }

  &__hatch {
    background: repeating-linear-gradient(-45deg, $hatchColor 0 1px, transparent 1px 0.4rem);
  }

  &__objective {
    position: absolute;
    top: 0;
    bottom: 0;
    border-left: 1px dashed $objectifColor;
    transform: translateX(-50%);
  }

  &__stat {
    position: absolute;
    top: 50%;
    white-space: nowrap;
    color: var(--text-title-grey);
    background-color: var(--background-default-grey);
    border-radius: 0.25rem;
    transform: translate(-50%, -50%);
  }
}
</style>
