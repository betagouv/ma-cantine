<template>
  <div>
    <p>Un produit de qualité et durable doit bénéficier d’un des labels suivants :</p>
    <ul id="about-labels">
      <li v-for="label in labels" class="label" :key="label.src">
        <img :src="require(`@/assets/quality-labels/${label.src}`)" :alt="label.title" :title="label.title"/>
        {{ label.text }}
      </li>
      <li>
        <i class='fas fa-check-square'></i>
        Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »
      </li>
      <li>
        <i class='fas fa-check-square'></i>
        Produit acquis suivant des modalités prenant en compte les coûts imputés aux externalités
        environnementales liées au produit pendant son cycle de vie (production, transformation,
        conditionnement, transport, stockage, utilisation) - À ce jour, il n’existe pas de référentiel
        ni de méthodologie offciels afin d’effectuer une sélection des produits alimentaires sur la base de ces coûts.
      </li>
      <li>
        <i class='fas fa-check-square'></i>
        Produits équivalents aux produits bénéficiant de ces mentions ou labels
      </li>
    </ul>
  </div>
</template>

<script>
  import labels from "@/data/quality-labels.json";

  export default {
    data() {
      return {
        labels
      }
    }
  }
</script>

<style scoped lang="scss">
  #about-labels {
    margin: 1em 0;

    li {
      margin: 1em 0;
    }
    
    .fa-check-square {
      color: $green;
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