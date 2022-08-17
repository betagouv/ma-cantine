<template>
  <router-link :to="to" exact :class="primary ? '' : 'mt-2 grey--text text--darken-1 caption'">
    <v-icon small class="mr-2" :color="primary ? 'primary' : ''">$arrow-left-line</v-icon>
    {{ text }}
  </router-link>
</template>

<script>
export default {
  props: {
    to: {
      type: Object,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
    primary: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
