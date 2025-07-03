<template>
  <div class="fr-text">
    <p>
      Les gestionnaires de cantines doivent informer leurs usagers et convives sur la qualité alimentaire (au sens
      EGalim) et nutritionnelle des repas servis. Pour en savoir plus sur cette mesure,
      <router-link :to="{ name: 'UnderstandingLaw' }">
        notre page dédiée.
      </router-link>
    </p>
    <p>
      Déclarez vos actions entreprises pour informer vos convives sur la qualité des repas.
    </p>
  </div>
</template>

<script>
export default {
  name: "InformationMeasureInfo",
}
</script>
