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
      >
        <source :src="mainVideo.video" />
        Votre navigateur ne peut pas afficher des vidéos.
      </video>
    </div>
    <p class="mt-2 mb-4" v-if="mainVideo && mainVideo.description">{{ mainVideo.description }}</p>
    <div v-if="suggestedVideos && suggestedVideos.length > 0">
      <h2 class="text-h6 mb-4">Autres webinaires</h2>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-for="video in suggestedVideos" :key="video.id">
          <v-card
            class="dsfr"
            :to="{ name: 'WebinairePage', params: { webinaireUrlComponent: `${video.id}--${video.title}` } }"
          >
            <v-card-title>{{ video.title }}</v-card-title>
            <v-card-text>{{ video.description }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "WebinairePage",
  components: { BreadcrumbsNav },
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
