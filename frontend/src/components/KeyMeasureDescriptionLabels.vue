<template>
  <div>
    <p>
      Les autres produits durables et de qualité au sens de l'objectif fixé par la loi EGalim sont ceux bénéficiant des
      labels / certifications / mentions suivantes :
    </p>
    <ul class="no-bullets">
      <li v-for="label in labels" class="label" :key="label.src">
        <img :src="`/static/images/quality-labels/${label.src}`" alt="" />
        {{ label.text }}
      </li>
      <li>
        <v-icon class="mb-1" :color="labelIcons.FERMIER.color">{{ labelIcons.FERMIER.icon }}</v-icon>
        Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »
      </li>
    </ul>
    <p>
      D'autres catégories permettent de comptabiliser les produits durables et de qualité, produits qui auront fait
      l'objet d'une sélection particulière lors de la procédure d'achat :
    </p>
    <ul class="no-bullets">
      <li>
        <v-icon class="mb-1" :color="labelIcons.EXTERNALITES.color">{{ labelIcons.EXTERNALITES.icon }}</v-icon>
        Produit acquis suivant des modalités prenant en compte les coûts imputés aux externalités environnementales
        liées au produit pendant son cycle de vie (production, transformation, conditionnement, transport, stockage,
        utilisation) - L'article 2152-10 du code de la commande publique dispose que, pour l'évaluation du coût du cycle
        de vie des produits, les acheteurs s'appuient sur une méthode accessible à tous, fondée sur des critères
        non-discriminatoires et vérifiables de manière objective et qui n'implique, pour les soumissionnaires, qu'un
        effort raisonnable dans la fourniture des données demandées. Ni la loi EGALIM, ni le code de la commande
        publique n'imposent de soumettre la méthodologie de calcul du coût des externalités environnementales liées aux
        produits à une validation de l'administration. Dès lors qu'ils respectent les exigences du code de la commande
        publique, les acheteurs ayant recours à ce mode de sélection sont libres de définir les modalités qui leur
        semblent les plus pertinentes sous leur responsabilité. Certaines démarches collectives et/ou certains
        fournisseurs accompagnent déjà les acheteurs dans la mise en place d'une méthode.
      </li>
      <li>
        <v-icon class="mb-1" :color="labelIcons.PERFORMANCE.color">{{ labelIcons.PERFORMANCE.icon }}</v-icon>
        Produits acquis principalement sur la base de leurs performances en matière environnementale et
        d'approvisionnements directs. Comme pour la catégorie précédente, les acheteurs s'appuient sur une méthode,
        qu'ils définissent, pour évaluer les deux critères cumulatifs (performance en matière environnementale et
        performance en matière d'approvisionnements directs), en fonction de caractéristiques non-discriminatoires,
        vérifiables de manière objective et qui n'impliquent, pour les soumissionnaires, qu'un effort raisonnable dans
        la fourniture des données demandées. Ni la loi EGALIM, ni le code de la commande publique n'imposent de
        soumettre la méthodologie d'évaluation des performances en matière de protection de l'environnement et de
        développement des approvisionnements directs liées aux produits à une validation de l'administration. Dès lors
        qu'ils respectent les exigences du code de la commande publique, les acheteurs ayant recours à ce mode de
        sélection sont libres de définir les modalités qui leur semblent les plus pertinentes sous leur responsabilité.
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Produits équivalents aux produits bénéficiants des labels, certifications ou mentions, en accord avec le code de
        la commande publique.
      </li>
    </ul>
  </div>
</template>

<script>
import labels from "@/data/quality-labels.json"
import Constants from "@/constants"

export default {
  data() {
    return {
      labels,
      labelIcons: Constants.MiscLabelIcons,
    }
  },
}
</script>

<style scoped lang="scss">
ul {
  margin: 1em 0;
  padding: 0;

  li {
    margin: 1em 0;
  }
}

.label {
  min-height: 3em;
}

.label > img {
  height: 2.9em;
  margin-right: 0.5em;
  float: left;
}
</style>
