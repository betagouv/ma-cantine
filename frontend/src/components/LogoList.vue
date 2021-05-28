<template>
  <div id="logos">
    <img
      v-for="label in labels"
      :key="label.title"
      :src="`/static/images/quality-labels/${label.src}`"
      :alt="label.title"
      :title="label.title"
    />
    <LogoBio />
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

#logos > img {
  max-height: 3em;
  margin: 0.1em;
}
</style>
