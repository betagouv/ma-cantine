<template>
  <div id="blogs-page">
    <router-view v-if="blogPosts" />
  </div>
</template>

<script>
export default {
  computed: {
    blogPosts() {
      return this.$store.state.blogPosts
    },
  },
}
</script>
