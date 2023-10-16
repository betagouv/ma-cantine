<template>
  <div>
    Appro Progress
    <div v-if="centralDiagnostic">Vos données appros sont fournis par votre cuisine centrale</div>
    <div v-else-if="diagnostic">Total HT : {{ diagnostic.valueTotalHt }}</div>
    <div v-else>Pas de diagnostic</div>
  </div>
</template>

<script>
export default {
  name: "ApproProgress",
  props: ["diagnostic", "centralDiagnostic"],
}
</script>
