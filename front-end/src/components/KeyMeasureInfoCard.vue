<template>
  <div class="measure-info-card">
    <div class="deadline">
      <h4><i class="far fa-calendar-alt"></i> Entrée en vigueur</h4>
      <p>{{ measure.deadline.display }}</p>
    </div>
    <div class="for-who">
      <h4><i class="fas fa-chart-pie"></i> Pour qui ?</h4>
      <p v-if="measure.who">{{measure.who}}</p>
      <div class="tags">
        <p class="tag" :class="tag" v-for="tag in measure.tags" :key="tag">
          {{ tagsInfo[tag] }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .measure-info-card {
    background: $light-green;
    border-radius: 15px;
    margin-right: 2em;
    padding: 1em 1.5em;
    width: 12em;
    flex-shrink: 0;
  }

  h4 {
    margin-top: 0.5em;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 1em;
    color: $grey;
  }

  .deadline > h2, .for-who > h2 {
    white-space: nowrap;
  }

  p {
    font-size: 14px;
    color: $black;
  }

  .tag {
    font-size: 14px;
    font-weight: bold;
    margin: 0.5em 0em;
    color: $green;
  }

  .fa-calendar-alt, .fa-chart-pie {
    color: $grey;
  }

  @media (max-width: 800px) {
    h4 {
      font-size: 16px;
    }
  }

  @media (max-width: 650px) {
    .measure-info-card {
      width: 70%;
    }

    .tags {
      column-count: 2;
    }
  }
</style>

<script>
  import tags from "@/data/sector-tags.json";

  export default {
    name: "KeyMeasureInfoCard",
    props: {
      measure: Object,
    },
    data() {
      return {
        tagsInfo: tags,
      }
    },
  };
</script>
