<script setup>
const props = defineProps(["objectives", "stats", "legends"])

const checkOutside = (index) => {
  const minValue = 5
  const checkStatsDifference = props.stats.length > 1
  if (checkStatsDifference) return Math.abs(props.stats[1] - props.stats[0]) < minValue && index === 0
  else return props.stats[index] < minValue
}
</script>

<template>
  <div class="graph-gauge fr-mb-3w" :class="{ 'fr-mt-7w': objectives, 'fr-mt-4w': !objectives }">
    <div v-if="objectives" class="graph-gauge__objectives-container">
      <p class="graph-gauge__objectif graph-gauge__objectif--title fr-text--sm ma-cantine--bold">
        Objectif EGalim
      </p>
      <p
        v-for="objectif in objectives"
        :key="objectif"
        :style="`left: ${objectif.value}%`"
        class="graph-gauge__objectif graph-gauge__objectif--marker fr-text--sm ma-cantine--bold"
        :class="{ alignRight: objectif.value === 100 }"
      >
        {{ objectif.name }}
      </p>
    </div>
    <div class="graph-gauge__bars-container">
      <div v-for="(stat, index) in stats" :key="stat" class="graph-gauge__bar" :style="`width: ${stat}%`">
        <p
          class="graph-gauge__stat fr-mb-0 ma-cantine--bold fr-text--sm fr-px-1w"
          :class="{ outside: checkOutside(index) }"
        >
          {{ stat }}%
        </p>
      </div>
    </div>
    <div class="graph-gauge__legends-container fr-mt-2w">
      <p v-for="legend in legends" :key="legend" class="graph-gauge__legend fr-mb-0">
        {{ legend }}
      </p>
    </div>
  </div>
</template>

<style lang="scss">
$graphHeight: 3rem;
$objectivesHeight: 1rem;
$dashColor: var(--green-emeraude-sun-425-moon-753);
$fillColor: var(--green-emeraude-main-632);
$legendSquareSize: 1rem;
$legendDashSize: calc($legendSquareSize / 5);

@function getDashedBackground($size: 0.5rem) {
  $dashSize: $size;
  $doubleDashSize: $dashSize * 2;
  @return repeating-linear-gradient(
    to left,
    $dashColor,
    $dashColor $dashSize,
    transparent $dashSize,
    transparent $doubleDashSize
  );
}

.graph-gauge {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;

  &__objectives-container {
    z-index: 1;
    position: relative;
    height: $objectivesHeight;
  }

  &__objectif {
    position: absolute;
    top: 0;
    transform: translateY(-100%);

    &--title {
      left: 0;
    }

    &--marker {
      &::before {
        content: "";
        height: calc($graphHeight + $objectivesHeight);
        border-width: 1px;
        border-style: dashed;
        border-color: black;
        position: absolute;
        bottom: 0;
        left: 0;
        transform: translateY(100%);
      }

      &.alignRight {
        transform: translateY(-100%) translateX(-100%);
        width: 10rem;
        text-align: right;
        &::before {
          right: 0;
          left: auto;
        }
      }
    }
  }

  &__bars-container {
    position: relative;
    border: solid 1px $dashColor;
    height: $graphHeight;
  }

  &__bar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    display: flex;
    justify-content: flex-end;
    align-items: center;

    &:first-child {
      background-color: $fillColor;
      color: $fillColor;
    }

    &:nth-child(2) {
      background: getDashedBackground();
      color: $dashColor;
    }
  }

  &__stat {
    color: white;

    &.outside {
      transform: translateX(100%);
      color: inherit;
    }
  }

  &__legends-container {
    display: flex;
    gap: 2rem;
  }

  &__legend {
    padding-left: 1.5rem;
    position: relative;

    &:before {
      content: "";
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: $legendSquareSize;
      height: $legendSquareSize;
      border-style: solid;
      border-width: 1px 0;
    }

    &:first-child {
      color: $fillColor;
      &:before {
        border-color: $fillColor;
        background-color: $fillColor;
      }
    }

    &:nth-child(2) {
      color: $dashColor;
      &:before {
        background-color: transparent;
        border-color: $dashColor;
        background: getDashedBackground($legendDashSize);
      }
    }
  }
}
</style>
