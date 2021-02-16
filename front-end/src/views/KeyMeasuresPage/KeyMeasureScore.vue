<template>
  <svg
    :height="radius * 2"
    :width="radius * 2"
  >
    <defs>
      <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#748852" />
        <stop offset="50%" stop-color="#E2A013" />
        <stop offset="100%" stop-color="#C13331" />
      </linearGradient>
    </defs>
    <text x="50%" y="50%" text-anchor="middle" stroke="#333" stroke-width="0.5px" dy=".3em">
      {{ score }} / {{ maxScore }}
    </text>
    <circle
      :stroke="colourForScore"
      fill="transparent"
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
      score: Number,
      maxScore: Number,
      radius: Number,
      stroke: Number
    },
    data() {
      const normalizedRadius = this.radius - this.stroke * 2;
      return {
        normalizedRadius,
        circumference: normalizedRadius * 2 * Math.PI
      }
    },
    computed: {
      strokeDashoffset() {
        const percentageScore = (this.score / this.maxScore) * 100;
        return this.circumference - percentageScore / 100 * this.circumference;
      },
      colourForScore() {
        let proportion = this.score / this.maxScore;
        if(proportion === 1) {
          return '#748852';
        } else if(proportion > 0.25) {
          return '#E2A013';
        } else {
          return '#C13331';
        }
      }
    }
  }
</script>

<style scoped>
  circle {
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
  }
</style>