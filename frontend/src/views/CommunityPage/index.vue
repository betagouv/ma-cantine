<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row class="my-4 align-center">
      <v-col cols="12" sm="2" class="pl-2 pr-2 pl-md-8 pr-md-0">
        <v-img src="/static/images/doodles-dsfr/primary/Hi.png" max-height="180" contain></v-img>
      </v-col>
      <v-col cols="12" sm="6" class="px-2 px-md-10 py-4">
        <h1 class="text-h4 font-weight-black">
          Par ici, on propose un espace d'entraide et rencontre, participez !
        </h1>
      </v-col>
      <v-col>
        <ul class="text-body-2">
          <li v-for="link in links" :key="link.title" class="my-1">
            <a :href="`#${link.id}`" v-if="link.id">
              <v-icon small color="primary">mdi-chevron-right</v-icon>
              {{ link.title }}
            </a>
            <router-link :to="link.to" v-else>
              <v-icon small color="primary">mdi-chevron-right</v-icon>
              {{ link.title }}
            </router-link>
          </li>
        </ul>
      </v-col>
    </v-row>

    <h3 class="font-weight-black text-h5 mt-8" id="precedents-evenements">Précedents webinaires à revoir</h3>
    <p class="my-4">
      Nos webinaires sont interactifs et permettent de poser vos questions aux intervenants. Vous pouvez toutefois
      regarder les replays !
    </p>

    <VideoTutorials
      id="evenements-passes"
      v-if="videoTutorials && videoTutorials.length > 0"
      :tutorials="videoTutorials"
    />

    <v-btn
      outlined
      color="primary"
      large
      class="mt-4 mb-8"
      href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/webinaires-les-defis-de-ma-cantine"
    >
      <v-icon class="mr-2">mdi-play-circle</v-icon>
      <span v-if="videoTutorials && videoTutorials.length > 0">Revoir les autres webinaires</span>
      <span v-else>Revoir les webinaires</span>
    </v-btn>

    <h2 class="font-weight-black text-h5" id="evenements">Webinaires à venir</h2>
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

    <v-divider class="my-10"></v-divider>
    <FacebookSection id="facebook" />

    <v-divider class="my-10"></v-divider>
    <TheNewsletter id="suivre" />
  </div>
</template>

<script>
import WebinaireCard from "./WebinaireCard"
import VideoTutorials from "./VideoTutorials"
import TheNewsletter from "@/components/TheNewsletter"
import FacebookSection from "./FacebookSection"
import { hideCommunityEventsBanner } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "CommunityPage",
  components: { WebinaireCard, TheNewsletter, FacebookSection, BreadcrumbsNav, VideoTutorials },
  data() {
    return {
      links: [
        {
          id: "precedents-evenements",
          title: "Précedents webinaires",
        },
        {
          id: "evenements",
          title: "Webinaires à venir",
        },
        {
          id: "facebook",
          title: "Rejoindre la communauté sur Facebook",
        },
        {
          to: { name: "BlogsHome" },
          title: "Notre blog",
        },
        {
          to: { name: "PartnersHome" },
          title: "Trouver des acteurs de l'éco-système",
        },
        {
          to: { name: "FaqPage" },
          title: "Foire aux questions",
        },
        {
          id: "suivre",
          title: "Suivre nos actus",
        },
      ],
    }
  },
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
