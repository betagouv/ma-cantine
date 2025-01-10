<template>
  <div>
    <p v-if="canteen.badges[badge.key]">{{ badge.subtitle }}</p>
    <p v-else-if="canteen.badges[badge.key] === false">
      Cet établissement ne respecte pas encore la loi EGalim pour cette mesure.
    </p>
    <p v-else>Pas de données disponibles.</p>
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
