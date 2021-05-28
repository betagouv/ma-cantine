<template>
  <div id="blogs-page">
    <router-view v-if="blogPosts" :key="$route.fullPath" />
  </div>
</template>

<script>
export default {
  computed: {
    blogPosts() {
      return this.$store.state.blogPosts
    },
  },
  mounted() {
    if (!this.blogPosts) this.$store.dispatch("fetchBlogPosts")
  },
}
</script>
