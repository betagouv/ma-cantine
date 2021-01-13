<template>
  <div id="presentation">
    <div class="presentation-content">
      <h1>Approvisionner ma cantine en denrées de qualité</h1>
      <div>
        La loi EGAlim vise à apporter une alimentation saine, de qualité et plus durable dans nos assiettes.
      </div>
      <div>
        Vous êtes en charge de l'approvisionnement d'une restauration collective ?
      </div>
      <div class="presentation-diagnostic">
        (bientôt disponible)
      </div>
    </div>
    <img src="@/assets/toque.svg" class="presentation-right-image">
  </div>

  <div id="main-goal">
    <h2>Les objectifs de la loi EGAlim</h2>
    <div id="key-goals">
      <div class="key-goal">
        <img src="@/assets/broco.png">
        <div>
          Promouvoir une alimentation saine et respectueuse de l'environnement.
        </div>
      </div>
      <div class="key-goal">
        <img src="@/assets/convive.png">
        <div>
          Réduire les inégalités d'accès à une alimentation durable et de qualité.
        </div>
      </div>
      <div class="key-goal">
        <img src="@/assets/checklist.png">
        <div>
          Assurer la juste rémunération des agriculteurs du secteur agricole.
        </div>
      </div>
    </div>
  </div>

  <div id="goal">
    <h2>Les enjeux de la loi EGAlim en restauration collective</h2>
    <div class="goal-information">
      Issu des Etats Généraux de l'Alimentation (EGA), la loi EGAlim pour
      l’équilibre des relations commerciales dans le secteur agricole et une
      alimentation saine et durable du 30 octobre 2018 (entrée en vigueur progressive).
      Elle utilise la restauration collective et ses 3 milliards de repas par an
      comme levier de la transition agricole et alimentaire.
    </div>
  </div>

  <div class="divider"></div>

  <div id="discover-measures">
    <h3>Les mesures phares de la loi EGAlim</h3>
    <h4>
      Découvrez les échéances de chaque mesure et des ressources pour vous
      aider à atteindre vos objectifs.
    </h4>
    <ol id="measures-list">
      <router-link
        v-for="measure in keyMeasures"
        :key="measure.id"
        :to="{ name: 'KeyMeasuresPage', hash: '#' + measure.id }"
        class="measure-link"
      >
        <li class="measure-item">
          <p class="measure-title">{{ measure.title }}</p>
          <p class="discover-measure">→ En savoir plus</p>
        </li>
      </router-link>
    </ol>
    <a id="download-documentation" download href="">
      Télécharger la documentation complète
    </a>
  </div>
</template>

<style scoped>
#presentation {
  display: flex;
  justify-content: space-around;
  padding: 20px;
}

.presentation-content {
  text-align: left;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 20px;
  color: rgba(0, 0, 0, 0.60);
}

h1, h2 {
  font-weight: bold;
  font-size: 37px;
  line-height: 52px;
  color: #EB5B25;
}

.presentation-diagnostic {
  text-align: center;
  max-width: 400px;
  height: 50px;
  line-height: 50px;
  color: white;
  background-color: #EB5B25;
  border-radius: 50px;
  font-weight: bold;
}

.presentation-right-image {
  width: 450px;
  height: 400px;
}

#main-goal {
  margin-top: 50px;
  background-color: #FDEFE9;
  padding: 30px;
}

#key-goals {
  display: flex;
  justify-content: space-evenly;
  margin: 30px 0;
}

.key-goal {
  width: 250px;
  font-size: 20px;
  line-height: 20px;
  color: #333333;
}

.key-goal > img {
  width: 60px;
  margin-bottom: 20px;
}

#goal {
  margin: 70px auto;
  max-width: 1200px;
}

.goal-information {
  font-weight: bold;
  font-size: 22px;
  line-height: 31px;
  color: rgba(0, 0, 0, 0.33);
}

.divider {
  height: 50px;
  background-image: url('../assets/divider-section.png');
}

#discover-measures {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 70px 0;
}

#discover-measures > h3 {
  font-weight: bold;
  font-size: 37px;
  text-align: center;
  color: #eb5b25;
  margin: 0.8em 0;
}

#discover-measures > h4 {
  font-size: 22px;
  text-align: center;
  color: #808080;
  max-width: 30em;
  margin: 0.5px 0;
}

#measures-list {
  padding: 0;
  margin: 5em 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  list-style: none;
}

a.measure-link {
  text-decoration: none;
  margin: 0.5em 0.7em;
}

.measure-item {
  background: rgba(240, 207, 137, 0.3);
  border-radius: 22px;
  height: 10em;
  width: 10em;
  border-radius: 22px;
  padding: 2em 1em;
  text-align: left;
  position: relative;
}

div.measure-text {
  height: 100%;
}

p.measure-title {
  font-weight: bold;
  font-size: 16px;
  color: #333333;
  margin: 0;
}

p.discover-measure {
  position: absolute;
  bottom: 2em;

  font-size: 16px;
  color: #333333;
}

#download-documentation {
  width: 423px;
  border-radius: 50px;
  background: #eb5b25;
  padding: 1em 0;

  text-decoration: none;
  font-weight: bold;
  font-size: 18px;
  line-height: 23px;
  text-align: center;
  color: rgba(255, 255, 255, 0.867527);

  /* TODO: supprimer quand on a le lien */
  display: none;
}
</style>

<script>
import keyMeasures from "@/data/key-measures.json";

export default {
  data() {
    return {
      keyMeasures,
    };
  },
};
</script>
