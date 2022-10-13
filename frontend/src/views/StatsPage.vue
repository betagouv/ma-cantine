<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="text-h4 font-weight-black black--text mb-6">Mesures d'impact, résultats 
    et statistiques d'usage de ma-cantine</h1>
    <div>
      <p v-for="(section, sectionIdx) in sections" :key="`a-${sectionIdx}`">
        <a :href="`#${normalise(section.title)}`">{{ section.title }}</a>
      </p>
    </div>
    <div v-for="(section, sectionIdx) in sections" :key="sectionIdx" class="mb-8">
      <h2 class="mb-4" :id="normalise(section.title)">{{ section.title }}</h2>
      <div v-for="(stat, idx) in section.stats" :key="idx" class="mb-4">
        <h3 class="mb-2">{{ stat.title }}</h3>
        <p class="explanation">{{ stat.explanation }}</p>
        <iframe
          :src="`https://ma-cantine-metabase.cleverapps.io${stat.link}`"
          frameborder="0"
          :width="stat.width || 800"
          :height="stat.height || 600"
          allowtransparency
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import stats from "@/data/stats-platform.json"

export default {
  name: "StatsPage",
  components: { BreadcrumbsNav },
  data() {
    return {
      sections: stats,
    }
  },
  methods: {
    normalise(title) {
      return title.replace(/ /g, "-")
    },
  },
}
</script>

<style scoped>
.explanation {
  white-space: pre-wrap;
}
</style>
