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
      <div class="point" v-for="(point, idx) in keyPoints" :key="point.id" :id="point.id">
        <div class="point">
          <p class="mesure-x">MESURE {{idx + 1}}</p>
          <h2>{{point.title}}</h2>
          <div class="tags" v-if="point.tags">
            <p v-for="tag in point.tags" :key="tag" :style="tags.find(element => element.id === tag).style">
              {{tags.find(element => element.id === tag).title}}
            </p>
          </div>
          <p class="deadline" v-if="point.deadline">{{point.deadline}}</p>
          <div v-for="subPoint in point.subPoints" :key="subPoint.id">
            <h3>{{subPoint.title}}</h3>
            <div class="tags" v-if="subPoint.tags">
              <p v-for="spTag in subPoint.tags" :key="spTag" :style="tags.find(element => element.id === spTag).style">
                {{tags.find(element => element.id === spTag).title}}
              </p>
            </div>
            <p class="deadline" v-if="subPoint.deadline">{{subPoint.deadline}}</p>
            <p class="description">{{subPoint.description}}</p>
          </div>
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

/* measures styling */
.point {
  margin: 1em;
}

p.mesure-x {
  font-weight: 400;
  margin-bottom: 0;
  font-size: 20px;
}

.tags {
  display: flex;
}

.tags > p {
  height: 20px;
  padding: 0.2em 1em;
  left: 0px;
  top: 0px;
  border-radius: 50px;
  color: #FFF;
  margin: 0 0.5em;
}

.deadline::before {
  content: "📅 ";
}

/* alternating alignment of measures content left and right */
#qualite-durable, #contre-gaspillage, #plastiques .point {
  text-align: left;
}

#information, #diversification {
  text-align: right;
}

#information .tags, #diversification .tags {
  justify-content: flex-end;
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
            "scolaire",
            "administration",
            "universitaire",
            "medical",
            "social",
            "creche",
            "loisirs",
            "entreprises"
          ],
          deadline: "1er janvier 2022",
          img: "@/assets/orange.png",
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
              title: "Information obligatoire des convives une fois par an",
              tags: [
                "scolaire",
                "administration",
                "universitaire",
                "medical",
                "social",
                "creche",
                "loisirs",
                "entreprises"
              ],
              deadline: "1er janvier 2022",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Information nutritionnelle",
              tags: [
                "scolaire",
                "universitaire",
                "creche",
              ],
              deadline: "30 octobre 2018",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Expérimentation de l’affichage de la nature des produits (facultatif)",
              tags: [
                "scolaire",
                "administration",
                "creche"
              ],
              deadline: "Du 14 avril 2019 au 31 octobre 2021",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
          ]
        },
        {
          id: "contre-gaspillage",
          title: "🙌🏻 Lutte contre le gaspillage alimentaire et dons alimentaires",
          tags: [
            "scolaire",
            "administration",
            "universitaire",
            "medical",
            "social",
            "creche",
            "loisirs",
            "entreprises"
          ],
          subPoints: [
            {
              title: "Diagnostic et démarches de lutte contre le gaspillage alimentaire",
              deadline: "22 octobre 2020",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Interdiction de rendre impropres à la consommation les excédents alimentaires encore consommables",
              deadline: "1er janvier 2020",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Proposition de convention de dons aux associations habilitées (si >3000 repas/jour)",
              deadline: "22 octobre 2020",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            }
          ]
        },
        {
          id: "diversification",
          title: "💪 Diversification des sources de protéines et menus végétariens",
          subPoints: [
            {
              title: "Plan pluriannuel de diversification des sources de protéines (si > 200 couverts/jour)",
              tags: [
                "scolaire",
                "administration",
                "social",
                "medical",
                "loisirs",
                "creche"
              ],
              deadline: "30 octobre 2018",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Expérimentation d’un menu végétarien par semaine",
              tags: [
                "scolaire",
              ],
              deadline: "Du 1er nov 2019 au 1er nov 2021",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            }
          ]
        },
        {
          id: "plastiques",
          title: "💨 Substitution des plastiques",
          subPoints: [
            {
              title: "Interdiction des ustensiles en plastique à usage unique",
              tags: [
                "scolaire",
                "administration",
                "social",
                "medical",
                "loisirs",
                "creche",
                "entreprises"
              ],
              deadline: "1er janvier 2020",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Interdiction des contenants alimentaires en plastique",
              tags: [
                "scolaire",
                "universitaire",
                "creche"
              ],
              deadline: "1er janvier 2025 / 2028 si < 2000 habitants",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            },
            {
              title: "Interdiction des bouteilles d’eau plate en plastique",
              tags: [
                "scolaire",
              ],
              deadline: "1er janvier 2020",
              description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            }
          ]
        }
      ],
      tags: [
        {
          id: "scolaire",
          title: "Scolaire",
          style: {
            "background-color": "#EB5C2E"
          }
        },
        {
          id: "administration",
          title: "Administration",
          style: {
            "background-color": "rgba(255,82,82,0.28)"
          }
        },
        {
          id: "universitaire",
          title: "Universitaire",
          style: {
            "background-color": "rgba(57,107,200,0.42)"
          }
        },
        {
          id: "medical",
          title: "Médical",
          style: {
            "background-color": "rgba(235,92,46,0.56)"
          }
        },
        {
          id: "social",
          title: "Social",
          style: {
            "background-color": "rgba(150,93,123,0.46)"
          }
        },
        {
          id: "creche",
          title: "Crèche",
          style: {
            "background-color": "rgba(249,168,38,0.31)"
          }
        },
        {
          id: "loisirs",
          title: "Loisirs",
          style: {
            "background-color": "rgba(159,97,106,1)"
          }
        },
        {
          id: "entreprises",
          title: "Entreprises",
          style: {
            "background-color": "rgba(57,107,200,1)"
          }
        }
      ]
    }
  },
}
</script>