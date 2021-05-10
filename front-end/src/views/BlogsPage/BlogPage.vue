<template>
  <div id="blog-page">
    <img src="@/assets/lighthouse.svg" alt="">
    <div id="content" v-html="html"></div>
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
      html: converter.makeHtml(require('@/assets/blog/'+this.id+".md").default)
    };
  }
}
</script>

<style scoped lang="scss">
  #blog-page {
    padding: 2em;
  }

  #content {
    text-align: left;
  }

  img {
    float: right;
    padding: 1em;
  }

  @media (max-width: 1000px) {
    img {
      display: none;
    }
  }
</style>