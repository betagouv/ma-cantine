<template>
  <div>HELLO WORLD: {{ webinaireUrlComponent }}</div>
</template>

<script>
export default {
  name: "WebinairePage",
  props: {
    webinaireUrlComponent: {
      type: String,
      required: true,
    },
  },
}
</script>
