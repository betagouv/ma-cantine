<template>
  <div class="fr-text">
    <p>
      Votre établissement, quelque soit son secteur d’activité, est déjà soumis à un certain nombre d’obligations pour
      réduire l'utilisation du plastique. D'autres obligations sont à venir. Pour en savoir plus,
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'interdiction-du-plastique' } }">
        notre page dédiée.
      </router-link>
    </p>
    <p>
      Déclarez vos actions entreprises sur ce thème pour évaluer votre situation et bénéficiez de ressources
      personnalisées : conseils pratiques sous forme d’articles, partenaires agréés, autres établissements dont
      s’inspirer...
    </p>
  </div>
</template>

<script>
export default {
  name: "NoPlasticMeasureInfo",
}
</script>
