<template>
  <div id="blogs-home">
    <div id="welcome-block">
      <h1>Découvrez notre espace blog et témoignages</h1>
      <img src="@/assets/lighthouse.svg" alt="">
    </div>

    <ol id="blogs-list">
      <router-link v-for="(post, idx) in posts" :key="idx" :to="{ name: 'BlogPage', params: { id: post.id } }" class="blog-card">
        <li>
          <h2>{{ post.meta.title }}</h2>
          <p class="date">{{ new Date(post.meta.date).toLocaleDateString("fr-FR", { year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
          <p class="tagline">{{ post.meta.tagline }}</p>
          <p class="read-more">Lire la suite</p>
        </li>
      </router-link>
    </ol>
  </div>
</template>

<script>
import { showdown } from 'vue-showdown';

export default {
  data() {
    const converter = new showdown.Converter({metadata: true});
    const postsContext = require.context("@/assets/blog/", true, /\.md$/);
    return {
      posts: postsContext.keys().map(filename => {
        // call makeHtml so getMetadata returns metadata
        converter.makeHtml(postsContext(filename).default);
        return {
          meta: converter.getMetadata(),
          id: filename.split('./')[1].split('.md')[0]
        };
      })
    };
  }
}
</script>

<style scoped lang="scss">
  #welcome-block {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2em;
    text-align: left;

    img {
      height: 15em;
      padding-left: 3em;
    }
  }

  #blogs-list {
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    padding: 2em;

    .blog-card {
      text-decoration: none;
      margin: 0.5em;
      color: $black;
      background: $light-yellow;
      width: 20em;
      min-height: 19em;
      border-radius: 22px;
      padding: 1em;
      text-align: left;
      position: relative;
      border-bottom: 3px solid $orange;
    }

    .date {
      color: $dark-grey;
      font-style: italic;
    }

    .read-more {
      background-color: $orange;
      color: $white;
      font-weight: bold;
      width: max-content;
      padding: 0.3em;
      position: absolute;
      bottom: 0.5em;
      right: 1em;
      transition: all ease .25s;
      border: 1px solid $light-yellow;
    }

    .read-more:hover {
      border-color: $orange;
      transform: scale(1.02);
    }
  }

  @media (max-width: 1000px) {
    #welcome-block {
      text-align: center;

      img {
        display: none;
      }
    }

    #blogs-list {
      justify-content: center;
      padding: 0;
    }
  }
</style>