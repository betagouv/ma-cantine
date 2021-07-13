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
}
</script>
