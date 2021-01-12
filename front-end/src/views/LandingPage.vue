<template>
  <div>
    <h1>Welcome</h1>
    <div id="discover-measures">
      <h3>Les mesures phares de la loi EGAlim</h3>
      <h4>Découvrez les échéances de chaque mesure et des ressources h4our vous aider à atteindre vos objectifs.</h4>
      <ol id="measures-list">
        <a href="" class="measure-link">
          <li class="measure-item">
            <p class="measure-title">🍎 Au moins 50% de produits de qualité et durables dont 20% de bio</p>
            <p class="discover-measure">→ En savoir plus</p>
          </li>
        </a>
      </ol>
      <a id="download-documentation" download href="">Télécharger la documentation complète</a>
    </div>
  </div>
</template>

<style scoped>
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
  color: #EB5B25;
}

#discover-measures > h4 {
  font-size: 22px;
  text-align: center;
  color: #808080;
  max-width: 872px;
}

#measures-list {
  padding: 0;
}

a.measure-link {
  text-decoration: none;
}

.measure-item {
  list-style: none;
  background: rgba(240, 207, 137, 0.3);
  border-radius: 22px;
  height: 240px;
  width: 196px;
  border-radius: 22px;
  padding: 36px 16px;
  text-align: left;
  position: relative;
}

p.measure-title {
  position: static;
  left: 8.16%;
  right: 8.16%;
  top: 15%;

  font-weight: bold;
  font-size: 16px;
  color: #333333;
}

p.discover-measure {
  position: absolute;
  bottom: 15%;

  font-size: 16px;
  color: #333333;
}

#download-documentation {
  width: 423px;
  border-radius: 50px;
  background: #EB5B25;
  padding: 1em 0;

  text-decoration: none;
  font-weight: bold;
  font-size: 18px;
  line-height: 23px;
  text-align: center;
  color: rgba(255, 255, 255, 0.867527);
}

</style>
