<template>
  <div>
    <div v-for="tutorial in sortedTutorials" :key="tutorial.category" class="my-4">
      <h3 class="mb-2">{{ tutorial.category }}</h3>
      <v-row>
        <v-col cols="12" sm="4" md="3" v-for="video in tutorial.videos" :key="video.id">
          <v-card class="video-card">
            <label :for="`video-${video.id}`" class="video-label text-body-2 font-weight-bold">{{ video.title }}</label>
            <video
              ref="video"
              :title="video.title"
              style="background: #333;"
              :poster="video.thumbnail"
              controls
              class="player"
              :id="`video-${video.id}`"
            >
              <source :src="video.video" />
              Votre navigateur ne peut pas afficher des vidéos.
            </video>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoTutorials",
  props: {
    tutorials: {
      type: Array,
      required: true,
    },
  },

  computed: {
    sortedTutorials() {
      return [
        {
          category: "Webinaires techniques : utilisation de la plateforme « ma cantine »",
          videos: this.tutorials.filter((x) => x.categories.indexOf("technical") > -1),
        },
        {
          category: "Transition alimentaire",
          videos: this.tutorials.filter((x) => x.categories.indexOf("transition") > -1),
        },
        {
          category: "Je suis...",
          videos: this.tutorials.filter((x) => x.categories.indexOf("profile") > -1),
        },
        {
          category: "Autres webinaires",
          videos: this.tutorials.filter((x) => !x.categories || x.categories.length === 0),
        },
      ].filter((x) => x.videos.length > 0)
    },
  },
}
</script>

<style scoped>
.player {
  height: 200px;
  overflow: hidden;
  width: 100%;
}
.video-label {
  position: absolute;
  color: white;
  margin-top: 0px;
  margin-left: 0px;
  text-shadow: 0px 0px 4px black;
  background-color: #00000053;
  padding: 2px 8px;
}
.video-card {
  position: relative;
}
</style>
