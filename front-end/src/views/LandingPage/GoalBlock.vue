<template>
  <div id="goal">
    <div class="goal-information">
      La restauration collective représente <b>près 4 milliards de repas/an !</b>
      Ces repas sont un levier de transition agricole et alimentaire fort.
    </div>
    <h3>Les enjeux pour la restauration collective</h3>
    <div class="goal-list">
      <ul>La loi EGAlim est issue des États Généraux de l'Alimentation (EGA). Elle permet :
        <li>✔️ <b>l'équilibre des relations</b> commerciales dans le secteur agricole.</li>
        <li>✔️ une entrée en vigueur progressive d'<b>une alimentation saine et durable</b></li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
  #goal {
    margin: 70px auto;
    max-width: 850px;
  }

  h3 {
    font-weight: bold;
    font-size: 37px;
    line-height: 52px;
    color: $green;
  }

  .goal-information {
    padding: 24px;
    border-radius: 20px;
    margin: auto;
    text-align: left;
    color: $green;
    background-color: $light-green;
    font-size: 20px;
  }

  .goal-list {
    margin: auto;
    margin-top: 30px;
    text-align: left;
    font-size: 20px;
    line-height: 35px;
    padding: 0 24px;
  }
</style>
