<template>
  <div id="key-measures">
    <div id="banner">
      <img src="@/assets/online-groceries.svg" id="groceries" alt="">
      <div id="banner-content">
        <h1>Les 5 mesures-phares de la loi EGAlim</h1>
        <div id="actions">
          <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
          <a id="about-cnrc" href="">Qu'est ce que le CNRC ?</a>
        </div>
      </div>
      <img src="@/assets/lighthouse.svg" id="lighthouse" alt="">
    </div>
    <div id="measures">
      <div class="measure" v-for="(measure, idx) in keyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <p class="measure-x">MESURE {{idx + 1}}</p>
          <h2>{{measure.title}}</h2>
          <div class="tags" v-if="measure.tags">
            <p class="tag" v-for="tag in measure.tags" :key="tag" :style="tags[tag].style">
              {{tags[tag].title}}
            </p>
          </div>
          <p class="deadline" v-if="measure.deadline">{{measure.deadline}}</p>
          <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
            <h3>{{subMeasure.title}}</h3>
            <div class="tags" v-if="subMeasure.tags">
              <p class="tag" v-for="spTag in subMeasure.tags" :key="spTag" :style="tags[spTag].style">
                {{tags[spTag].title}}
              </p>
            </div>
            <p class="deadline" v-if="subMeasure.deadline">{{subMeasure.deadline}}</p>
            <p class="description" v-if="subMeasure.htmlDescription" v-html="subMeasure.htmlDescription"></p>
            <p class="description" v-if="subMeasure.description">{{subMeasure.description}}</p>
          </div>
        </div>
        <div class="decorative-image">
          <img :src="measure.image" alt=""/>
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
  font-weight: 700;
}

#actions {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}

#guide-download {
  border-radius: 25px;
  background: rgb(0,191,113);
  color: #FFF;
  padding: 0.7em 2em;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

#about-cnrc {
  text-decoration: none;
  color: rgba(64,64,64,0.87);
  font-weight: 400;
  font-size: 17px;
}

#about-cnrc:visited {
  color: rgba(64,64,64,0.87);
}

/* measures styling */
.measure {
  display: flex;
  overflow: hidden;
  align-items: center;
}

.measure-content {
  margin: 2em;
}

.decorative-image {
  width: 20%;
}

p.measure-x {
  font-weight: 400;
  margin-bottom: 0;
  font-size: 24px;
}

h2 {
  font-size: 32px;
  font-weight: 700;
}

.tags {
  display: flex;
}

.tag {
  font-size: 12px;
  font-weight: 700;
  color: #FFF;
  text-align: center;
  line-height: 20px;

  border-radius: 50px;
  padding: 0 1em;
  margin: 0 0.3em;
}

.deadline {
  font-size: 18px;
  font-style: italic;
  font-weight: 400;
  line-height: 31px;
}

.deadline::before {
  content: "📅 ";
  font-style: normal;
}

h3 {
  font-size: 20px;
  font-weight: 400;
  line-height: 23px;
}

.description {
  font-size: 14px;
  font-weight: 400;
  line-height: 18px;
  white-space: pre-wrap;
}

/* alternating alignment of measures content left and right */
#qualite-durable, #contre-gaspillage, #plastiques {
  text-align: left;
}

#information, #diversification {
  text-align: right;
  flex-direction: row-reverse;
}

#information .tags, #diversification .tags {
  justify-content: flex-end;
}

#information div img, #diversification div img {
  position: relative;
  right: 250px;
}

</style>

<script>
export default {
  data() {
    return {
      keyMeasures: [
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
          subMeasures: [
            {
              id: "cinqante",
              title: "Au moins 50 % de produits de qualité et durables...",
              htmlDescription: "Les produits bénéficiant des autres signes officiels d’identification de la qualité et de l’origine (SIQO) ou des mentions valorisantes suivants : le <b>Label rouge</b>, l’<b>appellation d’origine (AOC/AOP)</b>, l’<b>indication géographique (IGP)</b>, la <b>Spécialité traditionnelle garantie (STG)</b>, la mention « issu d’une exploitation à <b>Haute Valeur Environnementale</b> » (HVE), la mention <b>« fermier » ou « produit de la ferme » ou « produit à la ferme »</b>, uniquement pour les produits pour lesquels existe une définition réglementaire des conditions de production*, l’<b>écolabel pêche durable, logo « Région ultrapériphérique » (RUP)</b>."
            },
            {
              id: "vingt",
              title: ".... dont au moins 20 % de produits biologiques",
              description: "L'ensemble des produits issus de l'agriculture biologique, ainsi que les produits végétaux en conversion de plus d'un an qui entrent également dans le décompte.\nIl ne peut s’agir que de produits bruts ou transformés composés d’un seul ingrédient d’origine végétale et issus d’une exploitation qui est en conversion depuis plus d’un an,"
            }
          ],
          image: require('@/assets/orange.png')
        },
        {
          id: "information",
          title: "👨‍👩‍👧‍👧 Information des usagers et convives",
          subMeasures: [
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
              description: "Les usagers des restaurants collectifs devront être informés une fois par an, par voie d’affichage et de communication électronique, de la part des produits de qualité et durables."
            },
            {
              title: "Information nutritionnelle",
              tags: [
                "scolaire",
                "universitaire",
                "creche",
              ],
              deadline: "30 octobre 2018",
              description: "Les gestionnaires des services de restauration collective scolaire et universitaire ainsi que des services de restauration collective des crèches sont tenus d’informer et de consulter régulièrement, dans chaque établissement et par tous moyens utiles, les usagers sur le respect de la qualité alimentaire et nutritionnelle des repas servis. La restauration scolaire fixe des exigences nutritionnelles basées sur 20 repas successifs. Il s’agit notamment de veiller à la diversité de la structure du repas, garantir une variété suffisante pour favoriser les apports en fibres et en fer, limiter la fréquence des plats trop gras et trop sucrés et de favoriser l’emploi de produits de saison."
            },
            {
              title: "Expérimentation de l’affichage de la nature des produits (facultatif)",
              tags: [
                "scolaire",
                "administration",
                "creche"
              ],
              deadline: "Du 14 avril 2019 au 31 octobre 2021",
              description: "À titre expérimental, pour une durée de 3 ans (soit jusqu’au 1er novembre 2021), les collectivités territoriales qui le souhaitent peuvent participer à une expérimentation sur l’affichage obligatoire, pour l’information des usagers, de la nature des produits entrant dans la composition des menus dans les services de restauration collective dont elles ont la charge."
            },
          ],
          image: require('@/assets/bleubronze.png')
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
          subMeasures: [
            {
              title: "Diagnostic et démarches de lutte contre le gaspillage alimentaire",
              deadline: "22 octobre 2020",
              description: "L’obligation de mettre en place une démarche de lutte contre le gaspillage alimentaire est étendue aux opérateurs de la restauration collective privée. À compter du 21 octobre 2019, les opérateurs de la restauration collective qui ne sont pas engagés dans une démarche de lutte contre le gaspillage alimentaire disposent d’un délai d’un an pour effectuer un diagnostic préalable à la mise en place de cette démarche, incluant l’approvisionnement durable."
            },
            {
              title: "Interdiction de rendre impropres à la consommation les excédents alimentaires encore consommables",
              deadline: "1er janvier 2020",
              description: "L’interdiction de rendre impropres à la consommation les excédents alimentaires encore consommables est étendue à la restauration collective (amende de 3 750 €) à partir du 1er janvier 2020."
            },
            {
              title: "Proposition de convention de dons aux associations habilitées (si >3000 repas/jour)",
              deadline: "22 octobre 2020",
              description: "Les opérateurs de la restauration collective préparant plus de 3 000 repas/jour disposent d’un délai d’un an pour proposer à une association habilitée en application de l’article L.266-2 du code de l’action sociale et des familles une convention de dons."
            }
          ],
          image: require('@/assets/saumon.png')
        },
        {
          id: "diversification",
          title: "💪 Diversification des sources de protéines et menus végétariens",
          subMeasures: [
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
              description: "Les gestionnaires des restaurants collectifs sont tenus de présenter à leurs structures dirigeantes un plan pluriannuel de diversification de protéines incluant des alternatives à base de protéines végétales dans les repas qu’ils proposent."
            },
            {
              title: "Expérimentation d’un menu végétarien par semaine",
              tags: [
                "scolaire",
              ],
              deadline: "Du 1er nov 2019 au 1er nov 2021",
              htmlDescription: "Tous les restaurants collectifs scolaires (publics ou privés) sont tenus de proposer, au moins une fois par semaine, un menu végétarien, sur une durée de 2 ans. Ce menu végétarien peut constituer une alternative à d’autres menus dans le cas où plusieurs menus sont proposés. Dans le cas où un menu unique est proposé, il s’agit d’un menu unique végétarien. Par ailleurs, le menu végétarien doit s’insérer dans un plan alimentaire respectueux des exigences relatives à la qualité nutritionnelle.\n<b>Qu’est-ce qu’un menu végétarien ?</b> Il s’agit d’un menu (toutes les composantes) sans viande, ni poisson, crustacés et fruits de mer. Il peut cependant comprendre des protéines animales (œufs, produits laitiers). Les alternatives protéiques utilisées peuvent être les légumineuses (lentilles, pois chiches, haricots...), les céréales (blé, riz, boulgour...), les œufs et/ou les produits laitiers."
            }
          ],
          image: require('@/assets/rose.png')
        },
        {
          id: "plastiques",
          title: "💨 Substitution des plastiques",
          subMeasures: [
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
              htmlDescription: "La mise à disposition des ustensiles à usage unique en matière plastique (sauf, jusqu’au 3 juillet 2021, ceux compostables en compostage domestique et constitués, pour tout ou partie, de matières biosourcées) suivants est <b>interdite : gobelets, verres, assiettes, pailles, couverts, piques à steak, couvercles à verre, plateaux-repas, pots à glace, saladiers, boîtes et bâtonnets mélangeurs pour boissons</b>. On entend par « mise à disposition » la fourniture d’un produit destiné à être distribué, consommé ou utilisé sur le territoire national dans le cadre d’une activité commerciale, à titre onéreux ou gratuit. Certains matériaux alternatifs au plastique peuvent être considérés comme des fournitures innovantes et entrer dans le cadre de l’expérimentation lancée fin 2018, pour une durée de trois ans, permettant de déroger aux obligations de publication et de mise en concurrence pour les achats innovants de moins de 100 000 € HT."
            },
            {
              title: "Interdiction des contenants alimentaires en plastique",
              tags: [
                "scolaire",
                "universitaire",
                "creche"
              ],
              deadline: "1er janvier 2025 / 2028 si < 2000 habitants",
              description: "L’utilisation de contenants alimentaires de cuisson, de réchauffe ou de service en matière plastique est interdite dans les services de restauration collective d’établissements scolaires et universitaires, ainsi que des établissements d’accueil des enfants de moins de 6 ans. Dans les collectivités territoriales de moins de 2 000 habitants, cette mesure est applicable au plus tard le 1er janvier 2028."
            },
            {
              title: "Interdiction des bouteilles d’eau plate en plastique",
              tags: [
                "scolaire",
              ],
              deadline: "1er janvier 2020",
              description: "L’utilisation de bouteilles d’eau plate en plastique est interdite en restauration scolaire. Cette mesure s’applique aux territoires desservis par un réseau d’eau potable et peut être suspendue en cas exceptionnel de restriction de l’eau destinée à la consommation humaine prononcée par le Préfet."
            }
          ],
          image: require('@/assets/vert.png')
        }
      ],
      tags: {
        scolaire: {
          title: "Scolaire",
          style: {
            "background-color": "#EB5C2E"
          }
        },
        administration: {
          title: "Administration",
          style: {
            "background-color": "rgba(255,82,82,0.28)"
          }
        },
        universitaire: {
          title: "Universitaire",
          style: {
            "background-color": "rgba(57,107,200,0.42)"
          }
        },
        medical: {
          title: "Médical",
          style: {
            "background-color": "rgba(235,92,46,0.56)"
          }
        },
        social: {
          title: "Social",
          style: {
            "background-color": "rgba(150,93,123,0.46)"
          }
        },
        creche: {
          title: "Crèche",
          style: {
            "background-color": "rgba(249,168,38,0.31)"
          }
        },
        loisirs: {
          title: "Loisirs",
          style: {
            "background-color": "rgba(159,97,106,1)"
          }
        },
        entreprises: {
          title: "Entreprises",
          style: {
            "background-color": "rgba(57,107,200,1)"
          }
        }
      }
    }
  },
}
</script>