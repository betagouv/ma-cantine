<template>
  <div>
    <div v-for="tutorial in sortedTutorials" :key="tutorial.category" class="my-4">
      <h3 class="mb-2">{{ tutorial.category }}</h3>
      <v-row>
        <v-col cols="12" sm="4" md="3" v-for="video in tutorial.videos" :key="video.id">
          <VideoTutorialCard :videoTutorial="video" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import VideoTutorialCard from "@/components/VideoTutorialCard"
export default {
  name: "VideoTutorials",
  components: { VideoTutorialCard },
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
