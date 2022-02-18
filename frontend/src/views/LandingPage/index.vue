<template>
  <div>
    <PresentationBlock class="mb-6" />

    <ActionsBlock class="ma-0 ma-md-n4 pa-6" style="background-color: #b6d9c8; border-radius: 16px;" />

    <v-divider class="mt-16"></v-divider>

    <KeyGoalsBlock class="mt-14 py-2" />

    <GoalBlock class="mt-16 py-2" />

    <DiscoverMeasuresBlock class="mt-16 py-2" />

    <v-divider class="mt-16"></v-divider>

    <Resources class="my-16" />

    <v-divider class="mt-16"></v-divider>

    <StartupPartners class="mt-16 mb-8" v-if="showPartners" />

    <v-divider class="mt-8"></v-divider>

    <TheNewsletter class="mt-12 mb-8" />
  </div>
</template>

<script>
import PresentationBlock from "@/views/LandingPage/PresentationBlock"
import ActionsBlock from "@/views/LandingPage/ActionsBlock"
import KeyGoalsBlock from "@/views/LandingPage/KeyGoalsBlock"
import GoalBlock from "@/views/LandingPage/GoalBlock"
import DiscoverMeasuresBlock from "@/views/LandingPage/DiscoverMeasuresBlock"
import Resources from "@/views/LandingPage/Resources"
import TheNewsletter from "@/components/TheNewsletter"
import StartupPartners from "@/views/LandingPage/StartupPartners"

export default {
  components: {
    PresentationBlock,
    ActionsBlock,
    KeyGoalsBlock,
    GoalBlock,
    DiscoverMeasuresBlock,
    TheNewsletter,
    Resources,
    StartupPartners,
  },
  computed: {
    showPartners() {
      return window.ENABLE_PARTNERS
    },
  },
}
</script>
