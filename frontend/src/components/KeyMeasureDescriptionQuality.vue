<template>
  <div id="appro-graphs">
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
    border: 3px solid;
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
