<script setup>
defineProps(["objectives", "stats", "legends"])
</script>

<template>
  <div class="graph-gauge">
    <div class="graph-gauge__objectives-container fr-mt-3w">
      <p class="graph-gauge__objectif graph-gauge__objectif--title fr-text--sm ma-cantine--bold">
        Objectif EGalim
      </p>
      <p
        v-for="(objectif, index) in objectives"
        :key="index"
        :style="`left: ${objectif}%`"
        class="graph-gauge__objectif graph-gauge__objectif--marker fr-text--sm ma-cantine--bold"
      >
        {{ objectif }}%
      </p>
    </div>
    <div class="graph-gauge__bars-container">
      <div
        v-for="(stat, index) in stats"
        :key="index"
        class="graph-gauge__bar"
        :class="{
          filled: index === 0,
          dashed: index === 1,
        }"
        :style="`width: ${stat}%`"
      ></div>
    </div>
    <div class="graph-gauge__legends-container fr-mt-2w">
      <p
        v-for="(legend, index) in legends"
        :key="index"
        class="graph-gauge__legend"
        :class="{
          filled: index === 0,
          dashed: index === 1,
        }"
      >
        {{ legend }} ({{ stats[index] }}%)
      </p>
    </div>
  </div>
</template>

<style lang="scss">
$graphHeight: 3rem;
$objectivesHeight: 1rem;
$bioColor: var(--green-emeraude-sun-425-moon-753);
$qualityColor: var(--green-emeraude-main-632);
$legendSquareSize: 1rem;
$legendDashSize: calc($legendSquareSize / 5);

@function getDashedBackground($size: 0.5rem) {
  $dashSize: $size;
  $doubleDashSize: $dashSize * 2;
  @return repeating-linear-gradient(
    to left,
    $bioColor,
    $bioColor $dashSize,
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
    }
  }

  &__bars-container {
    position: relative;
    border: solid 1px $bioColor;
    height: $graphHeight;
  }

  &__bar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
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
  }

  .dashed {
    &.graph-gauge__bar {
      background: getDashedBackground();
    }

    &.graph-gauge__legend {
      color: $bioColor;
      &:before {
        background-color: transparent;
        border-color: $bioColor;
        background: getDashedBackground($legendDashSize);
      }
    }
  }

  .filled {
    &.graph-gauge__bar {
      background: $qualityColor;
    }

    &.graph-gauge__legend {
      color: $qualityColor;
      &:before {
        border-color: $qualityColor;
        background-color: $qualityColor;
      }
    }
  }
}
</style>
