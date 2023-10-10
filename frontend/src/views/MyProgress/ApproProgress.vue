<template>
  <div>
    Appro Progress
    <div v-if="diagnostic">Total HT : {{ diagnostic.valueTotalHt }}</div>
    <div v-else>Pas de diagnostic</div>
  </div>
</template>

<script>
export default {
  name: "ApproProgress",
  props: ["diagnostic"],
}
</script>
