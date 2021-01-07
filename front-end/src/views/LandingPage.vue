<template>
  <div id="presentation">
    <div class="presentation-content">
      <h1>Mes approvisionnements sont-ils compatibles avec EGAlim ?</h1>
      <div class="presentation-information">
        <img src="@/assets/petitdej-dessin.svg" class="presentation-left-image">
        <div class="presentation-details">
          <div>
            Une des mesures-phare de la loi : à horizon 2022, au moins 50 % de produits
            de qualité et durables, dont au moins 20 % de produits biologiques dans
            les repas servis de votre cantine scolaire en gestion directe.
          </div>
          <div>
            <b>Vous êtes acheteur.ses et désirez savoir où vous en êtes dès aujourd’hui ?</b>
          </div>
          <div class="presentation-diagnostic">
            (bientôt disponible)
          </div>
        </div>
      </div>
    </div>
    <img src="@/assets/toque-dessin.svg" class="presentation-right-image">
  </div>

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
  width: 800px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

h1 {
  font-weight: bold;
  font-size: 37px;
  line-height: 52px;
  color: rgba(64, 64, 64, 0.85);
}

.presentation-information {
  display: flex;
  justify-content: space-around;
}

.presentation-left-image {
  width: 300px;
  height: 250px;
}

.presentation-details {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-weight: 600;
  font-size: 17px;
  line-height: 22px;
  color: rgba(0, 0, 0, 0.58);
}

.presentation-diagnostic {
  margin: 0 15%;
  height: 50px;
  line-height: 50px;
  color: white;
  background-color: #EB5B25;
  border-radius: 50px;
}

.presentation-right-image {
  width: 450px;
  height: 450px;
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
