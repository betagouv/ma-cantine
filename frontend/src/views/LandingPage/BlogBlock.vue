<template>
  <div v-if="visibleBlogPosts">
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="8">
        <h2 class="text-h4 font-weight-black">Les dernières actualités et partage d'expériences</h2>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row class="pa-4 mx-0 mx-md-n4 my-6 cta-group">
      <v-col cols="12" sm="6" md="4" v-for="post in visibleBlogPosts" :key="post.id">
        <BlogCard :post="post" />
      </v-col>
    </v-row>
    <v-btn large outlined color="primary" class="mt-2 mx-auto" :to="{ name: 'BlogsHome' }">
      <v-icon small class="mr-1">$newspaper-fill</v-icon>
      Visiter notre blog
    </v-btn>
  </div>
</template>

<script>
import BlogCard from "@/views/BlogsPage/BlogCard"

export default {
  name: "BlogBlock",
  components: { BlogCard },
  data() {
    return {
      visibleBlogPosts: null,
    }
  },
  methods: {
    fetchLatestBlogPosts() {
      this.$store
        .dispatch("fetchBlogPosts", { offset: 0, limit: 3, tag: null })
        .then((response) => {
          this.visibleBlogPosts = response.results
        })
        .catch(() => {
          console.error("error fetching latest blog posts")
        })
    },
  },
  mounted() {
    this.fetchLatestBlogPosts()
  },
}
</script>
