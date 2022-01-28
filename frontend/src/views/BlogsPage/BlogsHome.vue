<template>
  <div id="blogs-home">
    <v-card elevation="0" class="text-center text-md-left mb-10">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="100px" contain src="/static/images/lighthouse.svg"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="3" md="3" v-if="$vuetify.breakpoint.mdAndUp">
          <v-img max-height="200px" contain src="/static/images/lighthouse.svg"></v-img>
        </v-col>
        <v-col cols="12" sm="9" md="4">
          <v-card-title class="pr-0">
            <h1 class="font-weight-black text-h5 text-sm-h4">Découvrez notre espace blog et témoignages</h1>
          </v-card-title>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>

    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="4">
        <v-select
          v-model="tag"
          :items="tags"
          clearable
          hide-details
          id="select-tag"
          outlined
          class="mt-1"
          dense
          width="fit-content"
          label="Filtrer par type d'article"
        ></v-select>
      </v-col>
    </v-row>
    <div v-if="loading">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else>
      <v-pagination class="my-6" v-model="page" :length="Math.ceil(blogPostCount / limit)"></v-pagination>
      <v-progress-circular class="my-10" indeterminate v-if="!visibleBlogPosts"></v-progress-circular>
      <v-row v-else>
        <v-col cols="12" sm="6" md="4" v-for="post in visibleBlogPosts" :key="post.id">
          <BlogCard :post="post" />
        </v-col>
      </v-row>
      <v-pagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(blogPostCount / limit)"
        v-if="$vuetify.breakpoint.smAndDown"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import BlogCard from "./BlogCard"

export default {
  name: "BlogsHome",
  components: { BlogCard },
  data() {
    return {
      limit: 6,
      page: null,
      tag: null,
      filteredPosts: null,
    }
  },
  computed: {
    blogPostCount() {
      return this.posts && this.posts[0] ? this.posts[0].count : null
    },
    posts() {
      return this.filteredPosts || this.$store.state.blogPosts
    },
    visibleBlogPosts() {
      const blogPostPage = this.posts.find((x) => x.offset === this.offset)
      return blogPostPage ? blogPostPage.results : null
    },
    tags() {
      return this.$store.state.blogTags.map((x) => x.name)
    },
    loading() {
      if (this.tag && !this.filteredPosts) {
        return true
      }
      return this.blogPostCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
  },
  methods: {
    fetchCurrentPage() {
      if (!this.tag) {
        this.$store.dispatch("fetchBlogPosts", { offset: this.offset })
        this.filteredPosts = null
      } else {
        fetch(`/api/v1/blogPosts/?tag=${this.tag}&offset=${this.offset}&limit=6`)
          .then((response) => response.json())
          .then((data) => {
            this.filteredPosts = [{ ...data, limit: this.limit, offset: this.offset }]
          })
      }
    },
    updateRoute() {
      let query = { page: this.page }
      if (this.tag) {
        query.etiquette = this.tag
      }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query }).catch(() => {})
    },
  },
  watch: {
    page() {
      if (!this.visibleBlogPosts) this.fetchCurrentPage()
      this.updateRoute()
    },
    tag() {
      this.page = 1
      this.fetchCurrentPage()
      this.updateRoute()
    },
    $route(newRoute) {
      this.page = newRoute.query.page ? parseInt(newRoute.query.page) : 1
    },
  },
  mounted() {
    this.$store.dispatch("fetchBlogTags")
    this.tag = this.$route.query.etiquette
    this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
  },
}
</script>
