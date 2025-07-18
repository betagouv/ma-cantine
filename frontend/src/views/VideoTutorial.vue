<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'CommunityPage' } }]" :title="mainVideo ? mainVideo.title : ''" />
    <h1 v-if="mainVideo && mainVideo.title" class="font-weight-black text-h5 mb-4">{{ mainVideo.title }}</h1>
    <div>
      <video
        ref="video"
        :title="mainVideo.title"
        style="background: #333;"
        :poster="mainVideo.thumbnail"
        controls
        class="player"
        :id="`video-${mainVideo.id}`"
        crossorigin="anonymous"
        preload="metadata"
      >
        <source :src="mainVideo.video" />
        <track v-if="mainVideo.subtitles" label="Français" kind="subtitles" srclang="fr" :src="mainVideo.subtitles" />
        Votre navigateur ne peut pas afficher des vidéos.
      </video>
    </div>
    <p class="mt-2 mb-4" v-if="mainVideo && mainVideo.description">{{ mainVideo.description }}</p>
    <DsfrTranscription v-if="mainVideo.transcription">
      <div v-html="mainVideo.transcription"></div>
    </DsfrTranscription>
    <v-alert v-if="accessibilityProblem" type="info" outlined class="my-4">
      <p>
        {{ accessibilityProblem }} Si vous en avez besoin, contactez-nous avec notre
        <router-link :to="{ name: 'Contact' }">formulaire de contact</router-link>
        pour prioriser l'accessibilité de ce contenu.
      </p>
      <p class="mb-0">
        Pour plus d'informations consultez notre
        <router-link :to="{ name: 'Accessibilite' }">déclaration d'accessibilité</router-link>
      </p>
    </v-alert>
    <p v-else class="mt-4 text-right">
      Question, problème ?
      <router-link :to="{ name: 'Contact' }" class="grey--text text--darken-4">Contactez-nous</router-link>
    </p>
    <div v-if="suggestedVideos && suggestedVideos.length > 0" class="mt-6">
      <h2 class="text-h6 mb-4">Autres webinaires</h2>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-for="video in suggestedVideos" :key="video.id">
          <VideoTutorialCard :videoTutorial="video" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import VideoTutorialCard from "@/components/VideoTutorialCard"
import DsfrTranscription from "@/components/DsfrTranscription"

export default {
  name: "VideoTutorial",
  components: { BreadcrumbsNav, VideoTutorialCard, DsfrTranscription },
  props: {
    webinaireUrlComponent: {
      type: String,
      required: true,
    },
  },
  computed: {
    videoId() {
      return parseInt(this.webinaireUrlComponent.split("--")[0])
    },
    videoTutorials() {
      return this.$store.state.videoTutorials
    },
    mainVideo() {
      return this.videoTutorials.find((x) => x.id === this.videoId)
    },
    suggestedVideos() {
      return this.videoTutorials.filter((x) => x.id !== this.videoId)
    },
    accessibilityProblem() {
      let problem
      if (!this.mainVideo.subtitles && !this.mainVideo.transcription) {
        problem = "Cette vidéo n'a pas de sous-titres, ni de transcription."
      } else if (!this.mainVideo.subtitles) {
        problem = "Cette vidéo n'a pas de sous-titres."
      } else if (!this.mainVideo.transcription) {
        problem = "Cette vidéo n'a pas de transcription."
      }
      return problem
    },
  },
  watch: {
    mainVideo() {
      this.$refs.video.load()
      document.title = `Ma Cantine - webinaire « ${this.mainVideo?.title} »`
    },
  },
  beforeMount() {
    document.title = `Ma Cantine - webinaire « ${this.mainVideo?.title} »`
  },
}
</script>

<style scoped>
.player {
  height: 400px;
  overflow: hidden;
  width: 100%;
}
</style>
