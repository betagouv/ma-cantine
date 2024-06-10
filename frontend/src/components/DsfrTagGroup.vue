<template>
  <ul class="d-flex flex-wrap mx-n1 no-bullets">
    <li v-for="tag in tags" :key="tag.id">
      <DsfrTag :text="tag.text" :closeable="closeable" @close="closeable && closeAction(tag)" />
    </li>
  </ul>
</template>

<script>
import DsfrTag from "@/components/DsfrTag"

export default {
  name: "DsfrTagGroup",
  components: { DsfrTag },
  props: {
    tags: {
      type: Array,
      required: true,
    },
    closeable: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    closeAction(tag) {
      this.$emit("closeTag", tag)
    },
  },
}
</script>
