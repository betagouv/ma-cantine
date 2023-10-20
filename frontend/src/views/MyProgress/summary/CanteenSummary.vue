<template>
  <div>
    Canteen summary
  </div>
</template>

<script>
export default {
  name: "CanteenSummary",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
}
</script>
