<template>
  <div id="blogs-list">
    <div id="welcome-block">
      <h1> Découvrez notre espace témoignages </h1>
      <img src="@/assets/lighthouse.svg" alt="">
    </div>

    <div id="blogs">
      <router-link v-for="(post, idx) in posts" :key="idx" :to="{ name: 'BlogPage', params: { id: post.id } }" class="blog-card">
        <p>{{ post.meta.title }}</p>
        <p>{{ post.meta.date }}</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import { showdown } from 'vue-showdown';

export default {
  data() {
    const converter = new showdown.Converter({metadata: true});
    const postsContext = require.context("@/assets/blog/", true, /\.md$/);
    let posts = [];
    postsContext.keys().forEach(filename => {
      posts.push({
        html: converter.makeHtml(postsContext(filename).default),
        meta: converter.getMetadata(),
        id: filename.split('./')[1].split('.md')[0]
      });
    });
    return {
      posts
    };
  }
}
</script>

<style scoped lang="scss">
  #blogs {
    display: flex;

    .blog-card {
      border: 1px solid $black;
      width: min-content;
    }
  }

  #welcome-block {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3em;
    text-align: left;

    img {
      height: 15em;
      padding-left: 3em;
    }
  }

  @media (max-width: 1000px) {
    #welcome-block {
      text-align: center;

      img {
        display: none;
      }
    }
  }
</style>