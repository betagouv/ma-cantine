<template>
  <div>
    <div>HELLO WORLD: {{ webinaireUrlComponent }}</div>
    <div>Video url : {{ mainVideo.video }}</div>
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
}
</script>
