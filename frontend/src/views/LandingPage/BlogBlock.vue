<template>
  <div>
    <v-row v-if="visibleBlogPosts">
      <v-spacer></v-spacer>
      <v-col cols="12" sm="8">
        <h2 class="text-h4 font-weight-black">Les dernières actualités et partage d'expériences</h2>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row v-if="visibleBlogPosts">
      <v-col cols="12" sm="6" md="4" v-for="post in visibleBlogPosts" :key="post.id">
        <BlogCard :post="post" />
      </v-col>
      <v-col cols="12">
        <v-btn large outlined color="primary" :to="{ name: 'BlogsHome' }">
          <v-icon small class="mr-1">mdi-newspaper-variant-outline</v-icon>
          Voir plus
        </v-btn>
      </v-col>
    </v-row>
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
