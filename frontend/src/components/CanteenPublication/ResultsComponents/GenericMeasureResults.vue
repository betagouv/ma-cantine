<template>
  <div>
    <p v-if="canteen.badges[badge.key]">{{ badge.subtitle }}</p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>
  </div>
</template>

<script>
export default {
  name: "GenericMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnostics: Array,
  },
}
</script>
