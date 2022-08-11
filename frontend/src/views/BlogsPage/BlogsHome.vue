<template>
  <div id="blogs-home">
    <BreadcrumbsNav :links="[{ to: { name: 'CommunityPage' } }]" />
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
          @change="page = 1"
        ></v-select>
      </v-col>
    </v-row>
    <div v-if="loading" class="mt-8">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else>
      <v-pagination class="my-6" v-model="page" :length="Math.ceil(blogPostCount / limit)"></v-pagination>
      <v-progress-circular class="my-10" indeterminate v-if="!visibleBlogPosts"></v-progress-circular>
      <v-row v-else class="cta-group pa-2 mt-2">
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
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BlogCard from "./BlogCard"

export default {
  name: "BlogsHome",
  components: { BlogCard, BreadcrumbsNav },
  data() {
    return {
      limit: 6,
      page: null,
      tag: null,
      tags: [],
      visibleBlogPosts: null,
      blogPostCount: null,
    }
  },
  computed: {
    loading() {
      return this.blogPostCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
  },
  methods: {
    fetchCurrentPage() {
      this.$store
        .dispatch("fetchBlogPosts", { offset: this.offset, tag: this.tag })
        .then((response) => {
          this.tags = response.tags
          this.visibleBlogPosts = response.results
          this.blogPostCount = response.count
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    updateRoute() {
      let query = { page: this.page }
      if (this.tag) {
        query.etiquette = this.tag
      }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query }).catch(() => {})
    },
    populateParameters() {
      this.tag = this.$route.query.etiquette
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
    },
  },
  watch: {
    page() {
      this.updateRoute()
    },
    tag() {
      this.updateRoute()
    },
    $route(newRoute, oldRoute) {
      this.visibleBlogPosts = null
      if (newRoute.query.etiquette !== oldRoute.query.etiquette) {
        this.blogPostCount = null
      }
      this.populateParameters()
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.populateParameters()
    if (Object.keys(this.$route.query).length > 0) this.fetchCurrentPage()
  },
}
</script>
