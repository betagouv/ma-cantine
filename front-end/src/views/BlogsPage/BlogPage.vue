<template>
  <div id="content" v-html="html"></div>
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
  #content {
    text-align: left;
  }
</style>