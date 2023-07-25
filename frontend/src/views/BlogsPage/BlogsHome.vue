<template>
  <div id="blogs-home">
    <BreadcrumbsNav :links="[{ to: { name: 'CommunityPage' } }]" />
    <v-card elevation="0" class="text-center text-md-left mb-10">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="100px" contain src="/static/images/lighthouse.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="3" md="3" v-if="$vuetify.breakpoint.mdAndUp">
          <v-img max-height="200px" contain src="/static/images/lighthouse.png"></v-img>
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
      <v-col cols="12" sm="6" md="8">
        <DsfrSearchField
          v-model="searchTerm"
          placeholder="Rechercher par titre ou contenu"
          hide-details
          clearable
          :clearAction="clearSearch"
          :searchAction="search"
          label="Rechercher"
        />
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <DsfrSelect
          v-model="tag"
          placeholder="Tous types d'articles"
          :items="tags"
          clearable
          hide-details
          id="select-tag"
          class="mt-1"
          width="fit-content"
          label="Filtrer par type d'article"
          @change="page = 1"
        />
      </v-col>
    </v-row>
    <div v-if="searchTerm && visibleBlogPosts.length === 0" class="d-flex flex-column align-center py-10">
      <v-spacer></v-spacer>
      <v-icon large>mdi-inbox-remove</v-icon>
      <p class="text-body-1 grey--text text--darken-1 my-2">Cette recherche n'a pas permis de trouver d'article</p>
    </div>

    <div v-if="loading" class="mt-8">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-if="!loading && visibleBlogPosts.length > 0">
      <DsfrPagination class="my-6" v-model="page" :length="Math.ceil(blogPostCount / limit)" />
      <v-progress-circular class="my-10" indeterminate v-if="!visibleBlogPosts"></v-progress-circular>
      <v-row v-else class="cta-group pa-2 mt-2">
        <v-col cols="12" sm="6" md="4" v-for="post in visibleBlogPosts" :key="post.id">
          <BlogCard :post="post" />
        </v-col>
      </v-row>
      <DsfrPagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(blogPostCount / limit)"
        v-if="$vuetify.breakpoint.smAndDown"
      />
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BlogCard from "./BlogCard"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSearchField from "@/components/DsfrSearchField"

export default {
  name: "BlogsHome",
  components: { BlogCard, BreadcrumbsNav, DsfrSelect, DsfrPagination, DsfrSearchField },
  data() {
    return {
      limit: 6,
      page: null,
      tag: null,
      tags: [],
      visibleBlogPosts: null,
      blogPostCount: null,
      searchTerm: null,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
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
    search() {
      if (this.searchTerm && this.options.page !== 1) this.options.page = 1
      else this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      if (this.searchTerm) urlQueryParams["recherche"] = this.searchTerm
      return urlQueryParams
    },
    fetchCurrentPage() {
      if (this.searchTerm) {
        console.log("yo")
        let urlQueryParams = { page: this.options.page }
        console.log(urlQueryParams)
        urlQueryParams["recherche"] = this.searchTerm
      }
      this.$store
        .dispatch("fetchBlogPosts", { offset: this.offset, tag: this.tag, search: this.searchTerm })
        .then((response) => {
          this.tags = response.tags
          this.visibleBlogPosts = response.results
          this.blogPostCount = response.count
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    clearSearch() {
      this.searchTerm = ""
      this.fetchCurrentPage()
    },
    updateRoute() {
      let query = { page: this.page }
      if (this.tag) {
        query.etiquette = this.tag
      }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
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
