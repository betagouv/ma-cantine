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
          <v-card-title class="font-weight-black text-h5 text-sm-h4 pr-0">
            Découvrez notre espace blog et témoignages
          </v-card-title>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>

    <v-row>
      <v-col cols="12" sm="6" md="4" v-for="post in blogPosts" :key="post.id">
        <v-card
          class="fill-height text-left d-flex flex-column"
          hover
          :to="{ name: 'BlogPage', params: { id: post.id } }"
        >
          <v-card-title class="text-h6 font-weight-bold">{{ post.title }}</v-card-title>
          <v-card-subtitle class="pt-1">
            {{
              new Date(post.displayDate).toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" })
            }}
          </v-card-subtitle>
          <v-card-text>
            {{ post.tagline }}
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn outlined color="primary">
              Lire la suite
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
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
