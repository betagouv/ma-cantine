<template>
  <div>
    <p v-if="badge.earned">{{ badge.subtitle }}</p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>

    <p class="mb-0">
      Se renseigner sur
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: badge.id } }">
        la reglementation de la mesure « {{ badge.shortTitle }} »
      </router-link>
    </p>
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
