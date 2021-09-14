<template>
  <div class="poster-contents">
    <div id="heading">
      <div>
        <h2>Qualité des approvisionnements dans l’établissement {{ canteen.name || "_________" }}</h2>
        <div id="indicators">
          <!-- Can't use <img> because the object-fit is not respected in the PDF generation -->
          <div
            :style="`background-image: url('${canteen.mainImage}')`"
            v-if="canteen.mainImage"
            class="cantine-image"
            alt=""
          />

          <CanteenIndicators :canteen="canteen" />
        </div>
      </div>
      <div class="spacer"></div>
      <img src="/static/images/CoffeeDoodle.png" id="hat" alt="" />
    </div>

    <p id="introduction">
      Sur les {{ canteen.dailyMealCount }} repas servis aux convives, pour l’année 2020, voici la répartition, en valeur
      d’achat, des produits bio, de qualité et durables (liste de labels ci-dessous) utilisés dans la confection des
      repas
    </p>
    <div class="spacer"></div>

    <div id="graphs">
      <div>
        <p class="graph-title">Approvisionnement 2020</p>
        <SummaryStatistics :width="350" :qualityDiagnostic="diagnostic" class="summary-statistics" />
      </div>
      <div v-if="showPreviousDiagnostic">
        <p class="graph-title">Rappel 2019</p>

        <SummaryStatistics
          :hideLegend="true"
          :width="190"
          :qualityDiagnostic="previousDiagnostic"
          class="summary-statistics"
        />
      </div>
    </div>

    <LogoList id="logos" />

    <p v-if="patPercent" id="pat-percent">
      En plus, {{ patPercent }} % de produits dans le cadre de Projects Alimentaires Territoriaux
    </p>

    <div class="spacer"></div>
    <div id="about">
      <h3>Pourquoi je vois cette affiche ?</h3>
      <p>
        L’objectif de cet affichage est de rendre plus transparentes l’origine et la qualité des produits composant les
        menus et de soutenir l’objectif d’une alimentation plus saine et plus durable dans les restaurants. En
        partenariat avec ma-cantine.beta.gouv.fr; plateforme gouvernementale en expérimentation, cet établissement a
        rempli ses obligations d’information des convives.
      </p>
    </div>
    <div class="spacer"></div>
    <div id="more-information">
      <div class="footer-text">
        <p style="margin-bottom: 0px;">En savoir plus de la loi EGAlim :</p>
        <p><a href="https://ma-cantine.beta.gouv.fr/">https://ma-cantine.beta.gouv.fr/</a></p>
        <qrcode-vue
          v-if="canteen.publicationStatus !== 'published'"
          value="https://ma-cantine.beta.gouv.fr"
        ></qrcode-vue>
      </div>
      <div class="footer-text" style="text-align: right;" v-if="canteen.publicationStatus === 'published'">
        <p style="width: 210px;">En savoir plus sur les pratiques mises en oeuvre par l'établissement</p>
        <qrcode-vue :value="canteenUrl"></qrcode-vue>
      </div>
    </div>
  </div>
</template>

<script>
import LogoList from "@/components/LogoList"
import SummaryStatistics from "./SummaryStatistics"
import CanteenIndicators from "@/components/CanteenIndicators"
import QrcodeVue from "qrcode.vue"

export default {
  components: {
    LogoList,
    SummaryStatistics,
    CanteenIndicators,
    QrcodeVue,
  },
  props: {
    canteen: Object,
    diagnostic: Object,
    previousDiagnostic: Object,
  },
  computed: {
    patPercent() {
      const number = this.diagnostic.valuePatHt
      const total = this.diagnostic.valueTotalHt
      return !!number && !!total ? Math.round((100 * number) / total) : 0
    },
    showPreviousDiagnostic() {
      if (!this.previousDiagnostic) return false
      return !!this.previousDiagnostic.valueTotalHt
    },
    canteenUrl() {
      const baseUrl = window.location.toString().replace(window.location.pathname, "")
      const fullPath = this.$router.resolve({
        name: "CanteenPage",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
      }).href
      return baseUrl + fullPath
    },
  },
}
</script>

<style scoped lang="scss">
.poster-contents {
  display: flex;
  flex-direction: column;
  height: 296mm;
  overflow: hidden; // to show how it will be on paper
  padding: 14mm;
  // Need to repeat some styling directly here for PDF generation
  font-family: "Marianne";
}

// copy vuetify styling to have on generated PDF
p {
  margin-bottom: 16px;
}
i {
  background: white;
}

.spacer {
  flex-grow: 1;
}

#heading {
  display: flex;
  align-items: top;

  div {
    text-align: left;
  }

  h2 {
    font-size: 25px;
  }
}

.cantine-image {
  width: 150px;
  height: 75px;
  border-radius: 4px;
  margin-right: 8px;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

#indicators {
  margin: 8px 0 12px 0;
  font-size: 12px;
  line-height: 20px;
  color: rgba(0, 0, 0, 0.54);
  display: flex;
  align-items: center;
}

#hat {
  width: 150px;
  height: 112px;
  margin-left: 1em;
}

#introduction {
  font-size: 14px;
}

#logos {
  width: 440px;
  margin-bottom: 1.5em;
  margin-left: auto;
  margin-right: auto;
  align-self: center;
}

#graphs {
  align-self: center;
  display: flex;
  align-items: center;
}

.graph-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 8px;
}

#pat-percent {
  text-align: center;
  font-size: 13px;
}

#about {
  width: 100%;
  text-align: left;

  h3 {
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
  }
}

#more-information {
  width: 100%;
  display: flex;
  justify-content: space-between;

  a {
    color: $ma-cantine-grey;
    text-decoration: none;
    font-weight: bold;
  }

  .footer-text {
    font-size: 12px;
  }
}
</style>
