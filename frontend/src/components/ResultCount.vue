<template>
  <h2 aria-live="polite" aria-atomic="true">{{ count }} {{ count === 1 ? "résultat" : "résultats" }}</h2>
</template>

<script>
export default {
  name: "ResultCount",
  props: {
    count: {
      type: Number,
      required: true,
    },
  },
}
</script>
