<template>
  <ul class="d-flex flex-wrap mx-n1 no-bullets">
    <li v-for="tag in tags" :key="tag.id">
      <DsfrTag
        :text="tag.text"
        :icon="tag.icon"
        :closeable="closeable"
        @close="closeable && closeAction(tag)"
        :color="tag.color"
        :small="small"
        :clickable="clickable"
      />
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
    small: {
      type: Boolean,
      default: false,
    },
    clickable: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    closeAction(tag) {
      this.$emit("closeTag", tag)
    },
  },
}
</script>
