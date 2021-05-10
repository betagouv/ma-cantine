<template>
  <div id="blog-page">
    <img src="@/assets/lighthouse.svg" alt="">
    <h1>{{ meta.title }}</h1>
    <p class="date">Publié le {{ new Date(meta.date).toLocaleDateString("fr-FR", { year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
    <div id="content" v-html="html"></div>
    <router-link class="back-to-list" :to="{ name: 'BlogsHome' }">← Retour à la liste des articles</router-link>
  </div>
</template>

<script>
import { showdown } from 'vue-showdown';

export default {
  props: {
    id: String,
  },
  data() {
    const converter = new showdown.Converter({ metadata: true });
    return {
      html: converter.makeHtml(require('@/assets/blog/'+this.id+".md").default),
      meta: converter.getMetadata()
    };
  }
}
</script>

<style scoped lang="scss">
  #blog-page {
    padding: 2em;
    text-align: left;
  }

  img {
    float: right;
    padding: 1em;
  }

  .date {
    color: $dark-grey;
    font-style: italic;
  }

  #content {
    ::v-deep img {
      max-width: 100%;
    }

    ::v-deep ul {
      list-style: disclosure-closed;
      padding-left: 2.5em;
    }
  }

  .back-to-list {
    color: $orange;
    padding-top: 2em;
    display: block;
    text-align: right;
  }

  @media (max-width: 1000px) {
    img {
      display: none;
    }
  }
</style>