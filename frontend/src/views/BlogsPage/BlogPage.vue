<template>
  <div id="blog-page">
    <div v-if="blogPost">
      <v-card elevation="0" class="text-center text-md-left my-10">
        <v-row v-if="$vuetify.breakpoint.smAndDown">
          <v-col cols="12">
            <v-img max-height="100px" contain src="/static/images/lighthouse.svg"></v-img>
          </v-col>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="12" sm="3" v-if="$vuetify.breakpoint.mdAndUp">
            <v-img max-height="90px" contain src="/static/images/lighthouse.svg"></v-img>
          </v-col>
          <v-col cols="12" sm="9">
            <v-card-title class="font-weight-black text-h5 text-sm-h4">
              {{ blogPost.title }}
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

      <router-link :to="{ name: 'BlogsHome' }" class="my-10 d-block">← Retour à la liste des articles</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      blogPost: null,
    }
  },
  props: {
    id: {
      required: true,
    },
  },
  mounted() {
    const blogPost = this.$store.state.blogPosts.flatMap((x) => x.results).find((x) => x.id === parseInt(this.id))
    if (!blogPost) {
      return fetch(`/api/v1/blogPosts/${this.id}`)
        .then((response) => {
          if (response.status != 200) throw new Error()
          response.json().then((x) => (this.blogPost = x))
        })
        .catch(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cet article",
            status: "error",
          })
          this.$router.push({ name: "BlogsHome" })
        })
    }
    this.blogPost = blogPost
  },
  computed: {
    author() {
      if (!this.blogPost || !this.blogPost.author || !this.blogPost.author.firstName) return null
      return `${this.blogPost.author.firstName} ${this.blogPost.author.lastName}`
    },
  },
  watch: {
    blogPost() {
      if (this.blogPost) document.title = `${this.blogPost.title} - ma-cantine.beta.gouv.fr`
    },
  },
}
</script>

<style scoped>
#content >>> img {
  max-width: 100%;
  height: auto;
}
</style>
