<template>
  <div class="description-container">
    <p class="description" v-if="measure.htmlDescription" v-html="measure.htmlDescription"></p>
    <p class="description" v-else-if="measure.description">{{measure.description}}</p>
    <div id="appro-graphs" v-if="measure.id === 'qualite-des-produits'">
      <div>
        <p>Bons exemples :</p>
        <div class="good graphs">
          <img src="@/assets/appro-graphs/good-1.svg" class="graph" alt="Graphe du bon exemple : 20 % bio, 30 % durable (hors bio)" title="20 % bio, 30 % durable (hors bio)">
          <img src="@/assets/appro-graphs/good-2.svg" class="graph" alt="Graphe du bon exemple : 50 % bio, 0 % durable (hors bio)" title="50 % bio, 0 % durable (hors bio)">
        </div>
      </div>
      <div>
        <p>Mauvais exemples :</p>
        <div class="bad graphs">
          <img src="@/assets/appro-graphs/bad.svg" class="graph" alt="Graphe du mauvais exemple : 20 % bio, 20 % durable (hors bio)" title="20 % bio, 20 % durable (hors bio)">
          <img src="@/assets/appro-graphs/bad-1.svg" class="graph" alt="Graphe du mauvais exemple : 15 % bio, 50 % durable (hors bio)" title="15 % bio, 50 % durable (hors bio)">
        </div>
      </div>
      <div id="legend">
        <p><span class="dot bio"></span>Bio</p>
        <p><span class="dot durable"></span>Durable (hors bio)</p>
        <p><span class="dot other"></span>Autre</p>
      </div>
    </div>
    <div class="description" v-if="measure.id === 'cinquante'">
      <p>Un produit de qualité et durable doit bénéficier d’un des labels suivants :</p>
      <ul id="about-logos">
        <li v-for="logo in logos" class="logo" :key="logo.src">
          <img :src="require(`@/assets/logos/${logo.src}`)" :alt="logo.title" :title="logo.title"/>
          {{ logo.text }}
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
    <img
      v-if="measure.id === 'vingt'"
      id="bio-logo"
      src="@/assets/logos/logo_bio_eurofeuille.png"
      alt="Logo Agriculture Biologique"
      title="Logo Agriculture Biologique"
    >
  </div>
</template>

<script>
  const logos = [
    {
      src: "label-rouge.png",
      title: "Logo Label Rouge",
      text: "Label rouge - Signe national qui atteste qu’un produit possède un ensemble de caractéristiques spécifiques "+
        "établissant un niveau de qualité supérieur à celui d’un produit similaire."
    },
    {
      src: "Logo-AOC-AOP.png",
      title: "Logo Appellation d’origine (AOC/AOP)",
      text: "Appellation d’origine (AOC/AOP) - L’Appellation d’origine protégée (AOP) désigne un produit dont toutes les "+
        "étapes de production sont réalisées selon un savoir-faire reconnu dans une même aire géographique, "+
        "qui donne ses caractéristiques au produit."
    },
    {
      src: "IGP.png",
      title: "logo indication géographique",
      text: "Indication géographique (IGP) - L’Indication géographique protégée (IGP) identifie un produit agricole, "+
        "brut ou transformé, dont la qualité, la réputation ou d’autres caractéristiques sont liées à son origine géographique."
    },
    {
      src: "STG.png",
      title: "logo Spécialité traditionnelle garantie",
      text: "Spécialité traditionnelle garantie (STG) - Un produit dont les qualités spécifiques sont liées à une composition, "+
        "des méthodes de fabrication ou de transformation fondées sur une tradition."
    },
    {
      src: "hve.png",
      title: "logo Haute Valeur Environnementale",
      text: "Mention « issu d’une exploitation à Haute Valeur Environnementale » (HVE + niveau 2 accepté jusqu’au 31/12/2029)"
    },
    {
      src: "logo_label-peche-durable.png",
      title: "Écolabel pêche durable",
      text: "Écolabel pêche durable"
    },
    {
      src: "rup.png",
      title: "Logo Région Ultrapériphérique",
      text: "Logo « Région ultrapériphérique » (RUP) - Produits issus de 9 régions ultra-phériques à l’UE (Azores, Maderes, Canaries, Guadeloupe, Guyane, Martinique, à la Réunion, à Mayotte, Saint-Martin)"
    }
  ];

  export default {
    name: "KeyMeasureDescription",
    props: {
      measure: Object,
    },
    data() {
      return {
        logos
      }
    }
  }
</script>

<style scoped lang="scss">
  .description-container {
    flex: 4;

    /deep/ .fa-check-square, /deep/ .fa-arrow-alt-circle-right {
      color: $green;
    }
  }

  .description {
    font-size: 14px;
    font-weight: 400;
    line-height: 1.5em;
    white-space: pre-wrap;
  }

  #appro-graphs {
    display: flex;
    justify-content: space-between;
    align-items: center;

    p {
      margin-bottom: 0.6em;
      margin-left: 1em;
      font-size: 15px;
    }

    .graphs {
      border: 3px solid;
      border-radius: 0.5em;
      padding: 0.2em;
    }

    .good {
      border-color: $green;
      margin-right: 0.2em;
    }

    .bad {
      border-color: $red;
    }

    .graph {
      max-width: 50%;
    }
  }

  #legend {
    width: 11em;

    p {
      font-size: 0.8em;
    }

    .dot {
      height: 1em;
      width: 1em;
      border-radius: 50%;
      display: inline-block;
      margin-right: 0.3em;
    }

    .bio {
      background-color: #50b04E;
    }

    .durable {
      background-color: #fbbc04;
    }

    .other {
      background-color: #FFF4CA;
    }
  }

  #about-logos {
    li {
      margin: 1em 0;
    }
  }

  .logo {
    min-height: 3em;
  }

  .logo > img {
    height: 2.9em;
    margin-right: 0.5em;
    float: left;
  }

  #bio-logo {
    height: 2.9em;
    margin-top: 1em;
  }
</style>