<script setup>
defineProps(["objectives"])
</script>

<template>
  <div class="graph-quality-bio">
    <div class="graph-quality-bio__objectives-container fr-mb-2w">
      <p class="fr-text--sm ma-cantine--bold fr-mb-0">Objectif EGalim</p>
      <p
        class="graph-quality-bio__objectif fr-text--sm ma-cantine--bold"
        :style="`position: absolute; top: 0; left: ${objectives.bio}`"
      >
        {{ objectives.bio }}
      </p>
      <p
        class="graph-quality-bio__objectif fr-text--sm ma-cantine--bold"
        :style="`position: absolute; top: 0; left: ${objectives.quality}`"
      >
        {{ objectives.quality }}
      </p>
    </div>
    <div class="graph-quality-bio__bars-container">
      <div class="graph-quality-bio__bar filled" style="width: 35%"></div>
      <div class="graph-quality-bio__bar ashed" style="width: 16%"></div>
    </div>
    <div class="graph-quality-bio__legend-container">
      <p class="graph-quality-bio__legend ashed">
        bio et en conversion bio
      </p>
      <p class="graph-quality-bio__legend filled">
        durables et de qualité dont bio
      </p>
    </div>
  </div>
</template>

<style lang="scss">
$graphHeight: 3rem;
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
    border: solid 1px green;
    height: $graphHeight;
    margin-bottom: 2rem;
  }

  &__bar {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;

    &.ashed {
      background: blue;
      opacity: 0.5;
    }

    &.filled {
      background: aqua;
    }
  }

  &__legend-container {
    display: flex;
    gap: 1rem;
  }

  &__legend {
    padding-left: 2rem;
    position: relative;

    &:before {
      content: "";
      position: absolute;
      top: 50%;
      left: 0;
      width: 1rem;
      height: 1rem;
      background-color: inherit;
      transform: translateY(-50%);
    }

    &.ashed {
      color: blue;

      &:before {
        background-color: blue;
      }
    }

    &.filled {
      color: aqua;

      &:before {
        background-color: aqua;
      }
    }
  }
}
</style>
