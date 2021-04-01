<template>
  <div id="key-goals">
    <h2>Les objectifs de la loi EGAlim</h2>
    <div id="key-goals-list">
      <div class="key-goal">
        <img src="@/assets/broco.png" alt="">
        <p>Promouvoir une alimentation saine et respectueuse de l'environnement.</p>
      </div>
      <div class="key-goal">
        <img src="@/assets/convive.png" alt="">
        <p>Réduire les inégalités d'accès à une alimentation durable et de qualité.</p>
      </div>
      <div class="key-goal">
        <img src="@/assets/checklist.png" alt="">
        <p>Assurer la juste rémunération des agriculteurs du secteur agricole.</p>
      </div>
    </div>
    <a id="guide-cnrc" href="/Les mesures de la loi EGAlim restauration collective.pdf" download>
      Télécharger le livret de la loi EGAlim concernant la restauration collective <i class="fas fa-arrow-circle-down"></i>
    </a>
  </div>
</template>

<style scoped lang="scss">
  h2 {
    font-size: 37px;
    line-height: 52px;
    color: $orange;
  }

  #key-goals {
    margin-top: 50px;
    background-color: $light-orange;
    padding: 30px;
  }

  #key-goals-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    margin: 30px 0;
  }

  .key-goal {
    width: 250px;
    font-size: 20px;
    line-height: 20px;
    color: $grey;
    padding: 30px 0;
  }

  .key-goal > img {
    width: 60px;
  }

  #guide-cnrc {
    color: $orange;
    font-size: 20px;
  }
</style>
