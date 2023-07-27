<template>
  <div class="text-left">
    <h1 v-if="mainVideo && mainVideo.title" class="font-weight-black text-h5 mt-8">{{ mainVideo.title }}</h1>
    <div>
      <video
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
    <p v-if="mainVideo && mainVideo.description">{{ mainVideo.description }}</p>
    <div v-if="suggestedVideos && suggestedVideos.length > 0">
      <h2 class="text-h6">Autres webinaires</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "WebinairePage",
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
}
</script>

<style scoped>
.player {
  height: 400px;
  overflow: hidden;
  width: 100%;
}
</style>
