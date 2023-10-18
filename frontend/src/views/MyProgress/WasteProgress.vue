<template>
  <div class="pa-8 pb-4">
    <h3 class="fr-text font-weight-bold mb-4">
      {{ keyMeasure.title }}
    </h3>
    <div class="fr-text">
      <p>
        Votre établissement est soumis à l’obligation de faire une analyse des causes du gaspillage alimentaire, et de
        mettre en place une démarche de lutte contre le gaspillage alimentaire.
      </p>
      <p>
        Évaluez votre situation en déclarant les actions déjà entreprises, et bénéficiez ainsi de ressources
        personnalisées selon votre situation pour aller plus loin.
      </p>
      <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
    </div>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "WasteProgress",
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === "gaspillage-alimentaire")
    },
  },
}
</script>
