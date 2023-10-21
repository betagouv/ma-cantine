<template>
  <div class="fr-text">
    <p>
      Les gestionnaires de cantines doivent informer leurs usagers et convives sur la qualité alimentaire (au sens
      EGAlim) et nutritionnelle des repas servis. Pour en savoir plus sur cette mesure,
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }">
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
