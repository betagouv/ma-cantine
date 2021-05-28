<template>
  <div>
    <PresentationBlock />

    <ActionsBlock class="mt-16" />

    <v-divider class="mt-8"></v-divider>

    <KeyGoalsBlock class="mt-14 py-2" />

    <GoalBlock class="mt-16 py-2" />

    <DiscoverMeasuresBlock class="mt-16 py-2" />

    <v-divider class="mt-16"></v-divider>

    <TheNewsletter class="mt-12 mb-8" />
  </div>
</template>

<script>
import PresentationBlock from "@/views/LandingPage/PresentationBlock"
import ActionsBlock from "@/views/LandingPage/ActionsBlock"
import KeyGoalsBlock from "@/views/LandingPage/KeyGoalsBlock"
import GoalBlock from "@/views/LandingPage/GoalBlock"
import DiscoverMeasuresBlock from "@/views/LandingPage/DiscoverMeasuresBlock"
import TheNewsletter from "@/components/TheNewsletter"

export default {
  components: {
    PresentationBlock,
    ActionsBlock,
    KeyGoalsBlock,
    GoalBlock,
    DiscoverMeasuresBlock,
    TheNewsletter,
  },
}
</script>
