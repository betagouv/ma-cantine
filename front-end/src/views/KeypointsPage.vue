<template>
  <div>
    <div id="banner">
      <img src="@/assets/online-groceries.svg" id="groceries">
      <div id="banner-content">
        <h1>Les 5 mesures-phares de la loi EGAlim</h1>
        <div id="actions">
          <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
          <a id="cnrc" href="">Qu’est ce que le CNRC ?</a>
        </div>
      </div>
      <img src="@/assets/lighthouse.svg" id="lighthouse">
    </div>
    <div id="points">
      <div v-for="point in keyPoints" :key="point.id">
        <h2>{{point.title}}</h2>
        <div class="tags" v-if="point.tags">
          <p v-for="tag in point.tags" :key="tag">{{tags.find(element => element.id === tag).title}}</p>
        </div>
        <p class="deadline" v-if="point.deadline">{{point.deadline}}</p>
        <div v-for="subPoint in point.subPoints" :key="subPoint.id">
          <h3>{{subPoint.title}}</h3>
          <div class="tags" v-if="subPoint.tags">
            <p v-for="tag in subPoint.tags" :key="tag">{{tags.find(element => element.id === tag).title}}</p>
          </div>
          <p class="deadline" v-if="subPoint.deadline">{{subPoint.deadline}}</p>
          <p class="description">{{subPoint.description}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#banner {
  display: flex;
  justify-content: space-around;
  padding: 5em 10em;
}

#banner-content {
  width: 60%;
}

h1 {
  font-size: 37px;
  color: rgba(64,64,64,0.87);
}

#actions {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  font-size: 16px;
}

#guide-download {
  border-radius: 25px;
  background: rgb(0,191,113);
  color: #FFF;
  padding: 0.7em 2em;
  text-decoration: none;
  font-weight: 600;
}

#cnrc {
  text-decoration: none;
  color: rgba(64,64,64,0.87);
}

#cnrc:visited {
  color: rgba(64,64,64,0.87);
}

</style>

<script>
export default {
  data() {
    return {
      keyPoints: [
        {
          id: "qualite-durable",
          title: "🍎 Au moins 50% de produits de qualité et durables dont 20% de bio",
          tags: [
            "scolaire"
          ],
          deadline: "1er janvier 2022",
          subPoints: [
            {
              id: "cinqante",
              title: "Au moins 50 % de produits de qualité et durables...",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              id: "vingt",
              title: ".... dont au moins 20 % de produits biologiques",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            }
          ]
        },
        {
          id: "information",
          title: "👨‍👩‍👧‍👧 Information des usagers et convives",
          subPoints: [
            {
              id: "annual",
              title: "Information obligatoire des convives une fois par an",
              tags: [
                "scolaire"
              ],
              deadline: "1er janvier 2022",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              id: "nutrition",
              title: "Information nutritionnelle",
              tags: [
                "scolaire"
              ],
              deadline: "30 octobre 2018",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              id: "affichage",
              title: "Expérimentation de l’affichage de la nature des produits (facultatif)",
              tags: [
                "scolaire"
              ],
              deadline: "Du 14 avril 2019 au 31 octobre 2021",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
          ]
        },
      ],
      tags: [
        {
          id: "scolaire",
          title: "Scolaire",
          color: "#EB5C2E"
        }
      ]
    }
  },
}
</script>