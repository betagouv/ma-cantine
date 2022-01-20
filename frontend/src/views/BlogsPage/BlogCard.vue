<template>
  <v-card class="fill-height text-left d-flex flex-column" hover :to="{ name: 'BlogPage', params: { id: post.id } }">
    <v-card-title class="text-h6 font-weight-bold">{{ post.title }}</v-card-title>
    <v-card-subtitle class="pt-1">
      {{
        new Date(post.displayDate).toLocaleDateString("fr-FR", {
          year: "numeric",
          month: "long",
          day: "numeric",
        })
      }}
    </v-card-subtitle>
    <v-card-text>
      {{ post.tagline }}
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="pa-4">
      <v-chip v-if="tag" small :color="tag.colour">{{ tag.name }}</v-chip>
      <v-spacer></v-spacer>
      <v-btn outlined color="primary">
        Lire la suite
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "BlogCard",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      colours: [
        "pink lighten-4",
        "blue lighten-4",
        "teal lighten-4",
        "purple lighten-4",
        "green lighten-4",
        "yellow lighten-4",
      ],
    }
  },
  computed: {
    tags() {
      let tags = this.$store.state.blogTags
      tags.forEach((tag, idx) => (tag.colour = idx >= this.colours.length ? "" : this.colours[idx]))
      return tags
    },
    tag() {
      if (this.post.tags.length > 0) {
        return this.tags.find((x) => x.id == this.post.tags[0])
      }
      return undefined
    },
  },
}
</script>
