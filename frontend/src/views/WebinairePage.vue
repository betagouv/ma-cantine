<template>
  <div>
    <div v-if="mainVideo">
      <div>HELLO WORLD: {{ webinaireUrlComponent }}</div>
      <div>Video url : {{ mainVideo.video }}</div>
      <div>
        <router-link :to="{ name: 'WebinairePage', params: { webinaireUrlComponent: '2--notexist' } }">
          Next video
        </router-link>
      </div>
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
    videoTutorials() {
      return this.$store.state.videoTutorials
    },
    mainVideo() {
      const id = parseInt(this.webinaireUrlComponent.split("--")[0])
      return this.videoTutorials.find((x) => x.id === id)
    },
  },
  watch: {
    mainVideo(newVideo) {
      if (!newVideo) this.$router.push({ name: "NotFound" })
    },
  },
  beforeMount() {
    if (!this.mainVideo) this.$router.push({ name: "NotFound" })
  },
}
</script>
