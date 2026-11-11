<script setup>
import documentation from "@/data/documentation.json"
</script>

<template>
  <DsfrAlert title="Vous participez à l'expérimentation « Petites structures » ?" type="info" class="fr-mb-4w">
    <p>
      Pour cette première année, vous n'avez pas besoin de renseigner les familles de produits. Il vous suffit de suivre vos achats alimentaires en distinguant les produits bio des produits non bio. Pour savoir comment renseigner vos achats dans cet outil, consultez
      <a :href="documentation.petitesStructures" target="_blank">notre documentation dédiée</a>.
    </p>
  </DsfrAlert>
</template>
