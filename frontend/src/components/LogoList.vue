<template>
  <div id="logos">
    <div class="flex-column-center">
      <p class="label-title">Bio</p>
      <LogoBio />
    </div>
    <div class="separator"></div>
    <div class="flex-column-center">
      <p class="label-title">Qualité et durable (hors bio)</p>
      <div class="d-flex">
        <img
          v-for="label in labels"
          :key="label.title"
          :src="`/static/images/quality-labels/${label.src}`"
          :alt="label.title"
          :title="label.title"
        />
      </div>
    </div>
  </div>
</template>

<script>
import labels from "@/data/quality-labels.json"
import LogoBio from "@/components/LogoBio"

export default {
  components: {
    LogoBio,
  },
  data() {
    return {
      labels,
    }
  },
}
</script>

<style scoped lang="scss">
#logos {
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
}

#logos img {
  max-height: 30px;
  margin: 0 4px;
}

.separator {
  width: 1px;
  height: 50px;
  background: #ccc;
}

.flex-column-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.label-title {
  font-size: 0.875rem;
  font-weight: 700;
  line-height: 1.25rem;
  letter-spacing: 0.0178571429em;
  margin-bottom: 8px;
}
</style>
