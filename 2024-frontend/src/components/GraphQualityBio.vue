<script setup>
defineProps(["objectives", "results"])
</script>

<template>
  <div class="graph-quality-bio">
    <div class="graph-quality-bio__objectives-container fr-mb-2w">
      <p class="fr-text--sm ma-cantine--bold fr-mb-0">Objectif EGalim</p>
      <p class="graph-quality-bio__objectif fr-text--sm ma-cantine--bold" :style="`left: ${objectives.bio}`">
        {{ objectives.bio }}
      </p>
      <p class="graph-quality-bio__objectif fr-text--sm ma-cantine--bold" :style="`left: ${objectives.quality}`">
        {{ objectives.quality }}
      </p>
    </div>
    <div class="graph-quality-bio__bars-container fr-mb-2w">
      <div class="graph-quality-bio__bar filled" :style="`width: ${results.quality}`"></div>
      <div class="graph-quality-bio__bar dashed" :style="`width: ${results.bio}`"></div>
    </div>
    <div class="graph-quality-bio__legend-container">
      <p class="graph-quality-bio__legend dashed">bio et en conversion bio ({{ results.bio }})</p>
      <p class="graph-quality-bio__legend filled">durables et de qualité dont bio ({{ results.quality }})</p>
    </div>
  </div>
</template>

<style lang="scss">
$graphHeight: 3rem;
$bioColor: var(--green-emeraude-sun-425-moon-753);
$qualityColor: var(--green-emeraude-main-632);
$legendSquareSize: 1rem;
$legendDashSize: calc($legendSquareSize / 5);

@function getDashedBackground($size: 0.25rem) {
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

.graph-quality-bio {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;

  &__objectives-container {
    z-index: 1;
    position: relative;
  }

  &__objectif {
    position: absolute;
    top: 0;

    &::before {
      content: "";
      height: calc($graphHeight + 1rem);
      border-width: 1px;
      border-style: dashed;
      border-color: black;
      position: absolute;
      bottom: 0;
      left: 0;
      transform: translateY(100%);
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

  &__legend-container {
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
    &.graph-quality-bio__bar {
      background: getDashedBackground($legendDashSize);
    }

    &.graph-quality-bio__legend {
      color: $bioColor;
      &:before {
        background-color: transparent;
        border-color: $bioColor;
        background: getDashedBackground($legendDashSize);
      }
    }
  }

  .filled {
    &.graph-quality-bio__bar {
      background: $qualityColor;
    }

    &.graph-quality-bio__legend {
      color: $qualityColor;
      &:before {
        border-color: $qualityColor;
        background-color: $qualityColor;
      }
    }
  }
}
</style>
