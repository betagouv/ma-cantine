<template>
  <div>
    <p>
      La loi EGAlim et la loi Climat et Résilience encadrent la qualité des produits achetés entrant dans la composition
      des repas servis en restauration collective du secteur public et des établissements du secteur privé (article L.
      230-5 du Code Rural et de la Pêche Maritime). Les repas doivent comporter, à partir de l'année 2022, au moins 50 %
      de produits de qualité et durables dont au moins 20 % issus de l'agriculture biologique ou en conversion pour les
      cantines en France continentale (consulter
      <a href="https://ma-cantine.agriculture.gouv.fr/blog/16">notre blog</a>
      pour le seuil des autres régions).
    </p>
    <p>
      Ces taux (en %) sont calculés à partir de la valeur HT en euros de la somme des achats annuels alimentaires - sur
      l'ensemble des repas, boissons et collations comprises. i.e. Pour 100 euros d'achat, au moins 20 euros doivent
      correspondre à des produits bio ou en conversion et au total au moins 50 euros doivent correspondre à des produits
      durables et de qualité (bio inclus).
    </p>
    <div id="appro-graphs" class="mb-4">
      <div>
        <p>Exemple de ce qui est attendu fin 2022 :</p>
        <div class="good graphs">
          <img
            src="/static/images/appro-graphs/good-1.svg"
            class="graph"
            alt="Graphe du exemple satisfaisant fin 2022"
            title="20 % bio, 30 % durable (hors bio)"
          />
          <img
            src="/static/images/appro-graphs/good-2.svg"
            class="graph"
            alt="Graphe du exemple satisfaisant fin 2022"
            title="50 % bio, 0 % durable (hors bio)"
          />
        </div>
      </div>
      <div>
        <p>A améliorer d'ici fin 2022 :</p>
        <div class="bad graphs">
          <img
            src="/static/images/appro-graphs/bad-1.svg"
            class="graph"
            alt="Graphe du exemple insuffisant fin 2022"
            title="20 % bio, 20 % durable (hors bio)"
          />
          <img
            src="/static/images/appro-graphs/bad-2.svg"
            class="graph"
            alt="Graphe du exemple insuffisant fin 2022"
            title="15 % bio, 50 % durable (hors bio)"
          />
        </div>
      </div>
      <div id="legend">
        <p>
          <span class="dot bio"></span>
          Bio
        </p>
        <p>
          <span class="dot durable"></span>
          Durable (hors bio)
        </p>
        <p>
          <span class="dot other"></span>
          Autre
        </p>
      </div>
    </div>
    <p>
      Depuis la promulgation de la loi Climat et Résilience, l'ensemble de la restauration collective, publique comme
      privée, a l'obligation de proposer 50 % de produits de qualité dont 20 % de produits bio à compter de 2022 pour le
      public, et d'ici le 1er janvier 2024 pour la restauration collective du secteur privé. Depuis la promulgation de
      la loi Climat et Résilience, à partir du 1er janvier 2024, au moins 60% du total achat de la famille de denrées «
      viandes et poissons » est composé des produits de qualité et durables, ce taux étant fixé à 100% pour la
      restauration de l’Etat, ses établissements publics et les entreprises publiques nationales. La viande de synthèse
      est interdite en restauration collective. Le 1er janvier 2024, ces dispositions s’appliquent à tous les
      restaurants collectifs, y compris tous les restaurants d'entreprise (RE et RIE).
    </p>
  </div>
</template>

<style scoped lang="scss">
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
    border: 1px solid;
    border-radius: 0.5em;
    padding: 0.2em;
  }

  .good {
    border-color: $ma-cantine-green;
    margin-right: 0.2em;
  }

  .bad {
    border-color: $ma-cantine-red;
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
    background-color: #50b04e;
  }

  .durable {
    background-color: #fbbc04;
  }

  .other {
    background-color: #fff4ca;
  }
}

@media (max-width: 1120px) {
  #appro-graphs {
    flex-direction: column;

    .graphs {
      max-width: 25em;
    }
  }

  #legend {
    display: flex;
    width: 100%;
    justify-content: center;
  }
}
</style>
