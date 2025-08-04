<script setup>
defineProps(["objectives", "results"])

const graphHeight = 48
const spaceBetween = 16
</script>

<template>
  <svg class="graph-quality-bio" :height="graphHeight + spaceBetween">
    <defs>
      <pattern
        id="bio-dashed-background"
        patternTransform="rotate(90)"
        width="100%"
        height="8"
        x="0"
        y="0"
        patternUnits="userSpaceOnUse"
      >
        <rect x="0" y="0" width="100%" height="4" fill="transparent"></rect>
        <rect x="0" y="4" width="100%" height="4" class="bio"></rect>
      </pattern>
    </defs>
    <g>
      <rect class="qualityStroke" x="0" :y="spaceBetween" width="100%" :height="graphHeight"></rect>
      <rect class="quality" x="0" :y="spaceBetween" :width="results.quality" :height="graphHeight"></rect>
      <rect
        fill="url(#bio-dashed-background)"
        transform="scale(-1, 1)"
        transform-origin="center"
        x="0"
        :y="spaceBetween"
        :width="results.bio"
        :height="graphHeight"
      ></rect>
    </g>
    <g>
      <text x="0" y="0" class="fr-text--sm ma-cantine--bold">Objectif EGalim</text>
      <text :x="objectives.bio" y="0" class="fr-text--sm ma-cantine--bold">{{ objectives.bio }}</text>
      <text :x="objectives.quality" y="0" class="fr-text--sm ma-cantine--bold">{{ objectives.quality }}</text>
    </g>
    <g>
      <line
        :x1="objectives.bio"
        :y1="10"
        :x2="objectives.bio"
        :y2="graphHeight + spaceBetween"
        stroke="black"
        stroke-dasharray="4"
        stroke-width="2"
      />
      <line
        :x1="objectives.quality"
        :y1="10"
        :x2="objectives.quality"
        :y2="graphHeight + spaceBetween"
        stroke="black"
        stroke-dasharray="4"
        stroke-width="2"
      />
    </g>
    <g>
      <g>
        <text x="0" y="100%">
          <tspan width="16" height="16" x="0" y="100" fill="red"></tspan>
          bio et en conversion bio ({{ results.bio }})
        </text>
      </g>
    </g>
  </svg>
  <!--<figcaption class="graph-quality-bio__legend-container">
      <p class="graph-quality-bio__legend dashed"></p>
      <p class="graph-quality-bio__legend filled">durables et de qualité dont bio ({{ results.quality }})</p>
    </figcaption>
  </figure>-->
  <!--<br />
    <br />
    <br />
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
    <div class="graph-quality-bio__bars-container fr-mb-2w">
      <div class="graph-quality-bio__bar filled" :style="`width: ${results.quality}`"></div>
      <div class="graph-quality-bio__bar dashed" :style="`width: ${results.bio}`"></div>
    </div>-->
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
  // display: flex;
  // flex-direction: column;
  // justify-content: flex-start;
  // align-items: stretch;
  width: 100%;
  overflow: visible;

  & * {
    transform-box: fill-box;
  }

  .qualityStroke {
    stroke: $qualityColor;
    fill: transparent;
  }

  .quality {
    fill: $qualityColor;
  }

  .bio {
    fill: $bioColor;
  }

  // &__objectives-container {
  //   z-index: 1;
  //   position: relative;
  // }

  // &__objectif {
  //   &::before {
  //     content: "";
  //     height: calc($graphHeight + 1rem);
  //     border-width: 1px;
  //     border-style: dashed;
  //     border-color: black;
  //     position: absolute;
  //     bottom: 0;
  //     left: 0;
  //     transform: translateY(100%);
  //   }
  // }

  // &__bars-container {
  //   position: relative;
  //   border: solid 1px $bioColor;
  //   height: $graphHeight;
  // }

  // &__bar {
  //   position: absolute;
  //   left: 0;
  //   top: 0;
  //   height: 100%;

  //   &.dashed {
  //     background: getDashedBackground();
  //   }

  //   &.filled {
  //     background: $qualityColor;
  //   }
  // }

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

    &.dashed {
      color: $bioColor;

      &:before {
        border-color: $bioColor;
        background: getDashedBackground($legendDashSize);
      }
    }

    &.filled {
      color: $qualityColor;

      &:before {
        border-color: $qualityColor;
        background-color: $qualityColor;
      }
    }
  }
}
</style>
