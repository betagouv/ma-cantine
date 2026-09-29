<template>
  <div>
    <PresentationBlock class="my-12" />

    <ActionsBlock class="ma-0 ma-md-n4 pa-6 cta-group" />

    <DsfrCallout no-icon class="mt-16 py-8">
      <div class="text-left">
        <h2 class="text-h6 font-weight-bold mb-2">
          5 questions pour récolter votre avis sur la page d’accueil <em>ma cantine</em>
        </h2>
        <p class="text-body-2 mb-4">
          Vos retours son précieux, prenez quelques minutes pour nous les partager.
        </p>
        <v-btn color="primary" href="https://tally.so/r/VLKgBE" target="_blank" rel="noopener">
          Répondre à l’enquête
          <v-icon small class="ml-2">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
    </DsfrCallout>

    <v-divider aria-hidden="true" role="presentation" class="mt-16"></v-divider>

    <MissionBlock class="mt-14" />

    <v-divider aria-hidden="true" role="presentation" class="mt-16"></v-divider>

    <ToolsBlock class="mt-14" />

    <v-divider aria-hidden="true" role="presentation" class="mt-16"></v-divider>

    <KeyGoalsBlock class="mt-14 py-2" />

    <GoalBlock class="mt-16 py-2" />

    <DiscoverMeasuresBlock class="mt-16 py-2" />

    <v-divider aria-hidden="true" role="presentation" class="mt-16"></v-divider>

    <BlogBlock class="my-16" />

    <v-divider aria-hidden="true" role="presentation" class="mt-16"></v-divider>

    <Resources class="my-16" />

    <v-divider aria-hidden="true" role="presentation" class="mt-8"></v-divider>

    <TheNewsletter class="mt-12 mb-8" />
  </div>
</template>

<script>
import PresentationBlock from "@/views/LandingPage/PresentationBlock"
import ActionsBlock from "@/views/LandingPage/ActionsBlock"
import ToolsBlock from "@/views/LandingPage/ToolsBlock"
import KeyGoalsBlock from "@/views/LandingPage/KeyGoalsBlock"
import GoalBlock from "@/views/LandingPage/GoalBlock"
import DiscoverMeasuresBlock from "@/views/LandingPage/DiscoverMeasuresBlock"
import Resources from "@/views/LandingPage/Resources"
import TheNewsletter from "@/components/TheNewsletter"
import BlogBlock from "@/views/LandingPage/BlogBlock"
import MissionBlock from "@/views/LandingPage/MissionBlock"
import DsfrCallout from "@/components/DsfrCallout"

export default {
  components: {
    PresentationBlock,
    ActionsBlock,
    KeyGoalsBlock,
    GoalBlock,
    DiscoverMeasuresBlock,
    TheNewsletter,
    Resources,
    BlogBlock,
    MissionBlock,
    ToolsBlock,
    DsfrCallout,
  }
}
</script>
