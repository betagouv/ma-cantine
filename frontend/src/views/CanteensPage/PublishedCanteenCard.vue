<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    hover
    class="pa-4 text-left fill-height"
  >
    <v-card-title class="font-weight-black">
      {{ canteen.name }}
    </v-card-title>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city">
      <CanteenIndicators :canteen="canteen" />
    </v-card-subtitle>
    <v-card-text v-if="Object.keys(earnedBadges).length" class="grey--text text--darken-4 mx-1 mt-2">
      <v-row>
        <v-img
          max-width="30"
          contain
          :src="`/static/images/badge-${key}.svg`"
          v-for="(badge, key) in earnedBadges"
          :key="key"
          class="mx-1"
          :alt="badge.title"
          :title="badge.title"
        ></v-img>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { lastYear, earnedBadges } from "@/utils"

export default {
  name: "PublishedCanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: {
    CanteenIndicators,
  },
  data() {
    return {
      publicationYear: lastYear(),
    }
  },
  computed: {
    diagnostic() {
      return this.canteen.diagnostics.find((d) => d.year === this.publicationYear)
    },
    earnedBadges() {
      if (this.diagnostic) {
        return earnedBadges(this.canteen, this.diagnostic, this.$store.state.sectors)
      } else {
        return {}
      }
    },
  },
}
</script>
