<template>
  <div class="text-left">
    <v-row class="my-4 align-center">
      <v-col cols="12" sm="2" class="pl-2 pr-2 pl-md-8 pr-md-0">
        <v-img src="/static/images/doodles/primary/Hi.png" max-height="180" contain></v-img>
      </v-col>
      <v-col cols="12" sm="5" class="px-2 px-md-10 py-4">
        <h1 class="text-h5 font-weight-black">
          Par ici, on propose un espace d'entraide et rencontre, participez !
        </h1>
      </v-col>
      <v-col cols="12" sm="5" class="px-2 px-md-16 py-4">
        <div>
          <v-icon>mdi-chevron-right</v-icon>
          Webinaires
        </div>
        <div>
          <v-icon>mdi-chevron-right</v-icon>
          Contact
        </div>
        <div>
          <v-icon>mdi-chevron-right</v-icon>
          Être informé des événements
        </div>
      </v-col>
    </v-row>

    <v-divider class="mt-6 mb-10"></v-divider>

    <h2 class="font-weight-black text-h6">Webinaires à venir</h2>
    <p class="mt-4">
      Expertes et experts de la communauté partagent expériences et conseils pour développer votre carrière,
      inscrivez-vous pour y assister !
    </p>

    <v-row class="my-4">
      <v-col cols="12" v-for="webinaire in webinaires" :key="webinaire.id">
        <WebinaireCard :webinaire="webinaire" />
      </v-col>
      <v-col cols="12" v-if="webinaires.length === 0">
        <p><i>Aucun webinaire à venir, à bientôt !</i></p>
      </v-col>
    </v-row>

    <h3 class="font-weight-black body-1 mt-8">Précedents webinaires à revoir</h3>
    <p class="my-4">
      Nos webinaires sont interactifs et permettent de poser vos questions aux intervenants. Vous pouvez toutefois
      regarder les replays !
    </p>
    <v-btn outlined color="primary" large>
      <v-icon class="mr-2">mdi-play-circle</v-icon>
      Replay webinaires
    </v-btn>

    <v-divider class="mt-6 mb-10"></v-divider>
    <TheNewsletter />
  </div>
</template>

<script>
import WebinaireCard from "./WebinaireCard"
import TheNewsletter from "@/components/TheNewsletter"

export default {
  name: "CommunityPage",
  components: { WebinaireCard, TheNewsletter },
  computed: {
    webinaires() {
      return this.$store.state.upcomingCommunityEvents
    },
  },
}
</script>
