<template>
  <div id="blog-page">
    <div v-if="blogPost">
      <BreadcrumbsNav
        :title="blogPost.title"
        :links="[{ to: { name: 'CommunityPage' } }, { to: { name: 'BlogsHome' } }]"
      />
      <v-card elevation="0" class="text-center text-md-left my-10">
        <v-row v-if="$vuetify.display.smAndDown">
          <v-col cols="12">
            <v-img max-height="100px" contain src="/static/images/lighthouse.png"></v-img>
          </v-col>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="12" sm="3" v-if="$vuetify.display.mdAndUp">
            <v-img max-height="90px" contain src="/static/images/lighthouse.png"></v-img>
          </v-col>
          <v-col cols="12" sm="9">
            <v-card-title>
              <h1 class="font-weight-black text-h5 text-sm-h4">{{ blogPost.title }}</h1>
            </v-card-title>
            <v-card-subtitle>
              Publié le
              {{
                new Date(blogPost.displayDate).toLocaleDateString("fr-FR", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })
              }}
              <span v-if="author">par {{ author }}</span>
            </v-card-subtitle>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
      </v-card>
      <div id="content" v-html="blogPost.body" class="text-left"></div>

      <BackLink :to="backLink" text="Retour à la liste des articles" :primary="true" class="my-10 d-block" />
    </div>
  </div>
</template>

<script>
import BackLink from "@/components/BackLink"
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"

export default {
  components: {
    BackLink,
    BreadcrumbsNav,
  },
  data() {
    return {
      blogPost: null,
      backLink: { name: "BlogsHome" },
    }
  },
  props: {
    id: {
      required: true,
    },
  },
  mounted() {
    return fetch(`/api/v1/blogPosts/${this.id}`)
      .then((response) => {
        if (response.status !== 200) throw new Error()
        response.json().then((x) => (this.blogPost = x))
      })
      .catch(() => {
        this.$store.dispatch("notify", {
          message: "Nous n'avons pas trouvé cet article",
          status: "error",
        })
        this.$router.push({ name: "BlogsHome" })
      })
  },
  computed: {
    author() {
      if (!this.blogPost || !this.blogPost.author || !this.blogPost.author.firstName) return null
      return `${this.blogPost.author.firstName} ${this.blogPost.author.lastName}`
    },
  },
  watch: {
    blogPost() {
      if (this.blogPost) document.title = `${this.blogPost.title} - ${this.$store.state.pageTitleSuffix}`
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (from.name == "BlogsHome") {
        // keep filter settings in URL params
        vm.backLink = from
      }
    })
  },
}
</script>

<style scoped>
#content >>> img {
  max-width: 100%;
  height: auto;
}
</style>
