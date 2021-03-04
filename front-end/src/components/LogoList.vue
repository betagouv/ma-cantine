<template>
  <div id="logos">
    <img src="@/assets/logos/label-rouge.png" alt="logo Label Rouge"/>
    <img src="@/assets/logos/Logo-AOC-AOP.png" alt="logo appellation d’origine"/>
    <img src="@/assets/logos/IGP.png" alt="logo indication géographique"/>
    <img src="@/assets/logos/STG.png" alt="logo Spécialité traditionnelle garantie"/>
    <img src="@/assets/logos/hve.png" alt="logo Haute Valeur Environnementale"/>
    <img src="@/assets/logos/logo_label-peche-durable.png" alt="logo écolabel pêche durable"/>
    <img src="@/assets/logos/rup.png" alt="logo Région Ultrapériphérique"/>
    <img src="@/assets/logos/logo_bio_eurofeuille.png" alt="logo Agriculture Biologique"/>
  </div>
</template>

<style scoped lang="scss">
  #logos {
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
  }

  #logos > img {
    max-height: 3em;
    margin: 0.1em;
  }
</style>
