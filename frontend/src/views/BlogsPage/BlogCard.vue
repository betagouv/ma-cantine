<template>
  <v-card
    class="fill-height text-left d-flex flex-column dsfr"
    outlined
    :to="{ name: 'BlogPage', params: { id: post.id } }"
  >
    <v-card-title class="d-flex flex-column-reverse align-start">
      <component :is="hLevel" class="text-h6 font-weight-bold">{{ post.title }}</component>
      <ul class="mb-2 d-flex flex-wrap" v-if="post.tags && post.tags.length > 0">
        <li v-for="tag in post.tags" :key="tag">
          <v-chip small :color="tagColor(tag)" class="mr-1">
            <p class="mb-0">{{ tag }}</p>
          </v-chip>
        </li>
      </ul>
    </v-card-title>
    <v-card-subtitle class="pt-1">
      <p class="mb-0">
        {{
          new Date(post.displayDate).toLocaleDateString("fr-FR", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })
        }}
      </p>
    </v-card-subtitle>
    <v-card-text>
      <p class="mb-0">{{ post.tagline }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 py-4">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
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
    headingLevel: {
      type: String,
      required: false,
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
  computed: {
    hLevel() {
      return this.headingLevel || "h2"
    },
  },
}
</script>

<style scoped>
ul {
  padding-left: 0;
  list-style-type: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
li::before {
  content: "\200B";
}
</style>
