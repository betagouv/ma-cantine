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
      <div class="mb-2" v-if="post.tags && post.tags.length > 0">
        <v-chip v-for="tag in post.tags" small :color="tagColor(tag)" :key="tag" class="mr-1">{{ tag }}</v-chip>
      </div>
      {{ post.tagline }}
    </v-card-text>
    <v-spacer></v-spacer>
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
  methods: {
    tagColor(tag) {
      const colours = [
        "pink lighten-4",
        "blue lighten-4",
        "green lighten-4",
        "purple lighten-4",
        "yellow lighten-4",
        "teal lighten-4",
      ]
      const colourIndex = Array.from(tag, (x) => x.charCodeAt(0)).reduce((a, b) => a + b) % (colours.length - 1)
      return colours[colourIndex]
    },
  },
}
</script>
