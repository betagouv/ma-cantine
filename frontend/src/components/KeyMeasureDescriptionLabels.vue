<template>
  <div>
    <p>
      Un produit de qualité et durable au sens de l'objectif fixé par la loi EGAlim doit bénéficier d’un des labels
      suivants :
    </p>
    <ul id="about-labels">
      <li v-for="label in labels" class="label" :key="label.src">
        <img :src="`/static/images/quality-labels/${label.src}`" :alt="label.title" :title="label.title" />
        {{ label.text }}
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Produits issus du commerce équitable
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Produit acquis suivant des modalités prenant en compte les coûts imputés aux externalités environnementales
        liées au produit pendant son cycle de vie (production, transformation, conditionnement, transport, stockage,
        utilisation) - À ce jour, il n’existe pas de référentiel ni de méthodologie officiels afin d’effectuer une
        sélection des produits alimentaires sur la base de ces coûts. Les acheteurs ayant recours à ce mode de sélection
        sont libres de définir les modalités qui leur semblent les plus pertinentes sous réserve qu'elles respectent les
        conditions de recours à une telle évaluation fixées par le code de la commande publique.
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Produits acquis principalement sur la base de leurs performances en matière environnementale et
        d’approvisionnements directs (précisions à venir)
      </li>
      <li>
        <v-icon color="green" small>mdi-checkbox-marked</v-icon>
        Produits équivalents aux produits bénéficiant de ces signes, mentions ou labels
      </li>
    </ul>
  </div>
</template>

<script>
import labels from "@/data/quality-labels.json"

export default {
  data() {
    return {
      labels,
    }
  },
}
</script>

<style scoped lang="scss">
#about-labels {
  margin: 1em 0;
  list-style-type: none;
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
