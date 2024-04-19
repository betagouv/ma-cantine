<template>
  <div>
    <p v-if="badge.earned">{{ badge.subtitle }}</p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>
  </div>
</template>

<script>
export default {
  name: "GenericMeasureResults",
  props: {
    badge: Object,
  },
}
</script>
