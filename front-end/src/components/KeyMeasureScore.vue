<template>
  <svg
    :height="radius * 2"
    :width="radius * 2"
  >
    <title>Score d'achèvement pour "{{ measure.title }}"</title>
    <text x="50%" y="50%" text-anchor="middle" stroke-width="0.5px" dy=".3em">
      {{ score }} / {{ maxScore }}
    </text>
    <circle
      class="background"
      fill="none"
      :stroke-dasharray="circumference + ' ' + circumference"
      :stroke-width="stroke"
      :r="normalizedRadius"
      :cx="radius"
      :cy="radius"
    />
    <circle
      :class="classForScore"
      fill="none"
      :stroke-dasharray="circumference + ' ' + circumference"
      :style="{ strokeDashoffset: strokeDashoffset }"
      :stroke-width="stroke"
      :r="normalizedRadius"
      :cx="radius"
      :cy="radius"
    />
  </svg>
</template>

<script>
  export default {
    props: {
      measure: Object,
      radius: Number,
      stroke: Number
    },
    data() {
      const normalizedRadius = this.radius - this.stroke * 2;
      return {
        normalizedRadius,
        circumference: normalizedRadius * 2 * Math.PI,
        maxScore: this.measure.subMeasures.length
      }
    },
    computed: {
      score() {
        let score = 0;
        this.measure.subMeasures.forEach(subMeasure => {
          if(subMeasure.status === 'done') {
            score += 1;
          } else if(subMeasure.status === 'planned') {
            score += 0.5;
          }
        });
        return score;
      },
      strokeDashoffset() {
        const percentageScore = (this.score / this.maxScore) * 100;
        return this.circumference - percentageScore / 100 * this.circumference;
      },
      classForScore() {
        let proportion = this.score / this.maxScore;
        if(proportion === 1) {
          return "green";
        } else if(proportion > 0.25) {
          return "yellow";
        } else {
          return "red";
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  text {
    stroke: $grey;
  }

  circle {
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
  }

  circle.background {
    stroke: $dark-white;
  }

  circle.red {
    stroke: $red;
  }

  circle.yellow {
    stroke: $yellow;
  }

  circle.green {
    stroke: $green;
  }
</style>