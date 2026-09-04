<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row class="my-4">
      <v-col cols="12" class="pl-2 pr-2">
        <h1 class="text-h4 font-weight-black">
          Les webinaires
        </h1>
      </v-col>
    </v-row>

    <h2 class="font-weight-black text-h5" id="evenements">À venir</h2>
    <p class="my-4">
      Membres de la communauté partagent expériences et conseils pour utiliser notre plateforme et améliorer votre
      offre, inscrivez-vous pour y assister !
    </p>

    <v-row class="mx-0 my-6 pa-6 cta-group">
      <v-col cols="12" v-for="webinaire in webinaires" :key="webinaire.id">
        <WebinaireCard :webinaire="webinaire" />
      </v-col>
      <v-col cols="12" v-if="webinaires.length === 0">
        <p class="mb-0">Aucun webinaire à venir, à bientôt !</p>
      </v-col>
    </v-row>

    <h3 class="font-weight-black text-h5 mt-8" id="precedents-evenements">À revoir</h3>
    <p class="my-4">
      Nos webinaires sont interactifs et permettent de poser vos questions aux intervenants. Vous pouvez toutefois
      regarder les replays !
    </p>

    <VideoTutorials
      id="evenements-passes"
      v-if="videoTutorials && videoTutorials.length > 0"
      :tutorials="videoTutorials"
    />

    <v-divider aria-hidden="true" role="presentation" class="my-10"></v-divider>
    <TheNewsletter id="suivre" />
  </div>
</template>

<script>
import WebinaireCard from "./WebinaireCard"
import VideoTutorials from "./VideoTutorials"
import TheNewsletter from "@/components/TheNewsletter"
import { hideCommunityEventsBanner } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "CommunityPage",
  components: { WebinaireCard, TheNewsletter, BreadcrumbsNav, VideoTutorials },
  computed: {
    webinaires() {
      return this.$store.state.upcomingCommunityEvents
    },
    videoTutorials() {
      return this.$store.state.videoTutorials
    },
  },
  mounted() {
    hideCommunityEventsBanner(this.webinaires, this.$store)
  },
}
</script>

<style scoped>
ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
