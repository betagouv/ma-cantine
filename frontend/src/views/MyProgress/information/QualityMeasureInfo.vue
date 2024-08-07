<template>
  <div class="fr-text">
    <p>
      Depuis 2022, les repas doivent comporter au moins {{ applicableRules.qualityThreshold }} % de produits de qualité
      et durables, dont au moins {{ applicableRules.bioThreshold }} % issus de l’agriculture biologique ou en
      conversion, pour les cantines
      {{
        applicableRules.hasQualityException ? `dans la région « ${regionDisplayName} »` : "en France métropolitaine"
      }}.
    </p>
    <p>Faites le bilan de vos achats pour :</p>
    <ul class="mb-4">
      <li>
        <b>vous situer</b>
        par rapport à ces objectifs,
      </li>
      <li>
        bénéficier de
        <b>ressources personnalisées</b>
        selon votre situation pour vous améliorer,
      </li>
      <li>
        <b>informer vos convives</b>
        directement sur la plateforme ma cantine ou en générant facilement une affiche,
      </li>
      <li>
        et
        <b>participer aux campagnes annuelles de collecte de données d’achat</b>
        pour permettre d’établir le bilan statistique national.
      </li>
    </ul>
    <p>
      Pour cela, vous avez besoin a minima de connaître la valeur totale de vos achats de l’année, et les valeurs
      totales d’achats bios, de qualité, et durables.
    </p>
    <p>
      Pour vous aider à vous préparer à la saisie de vos valeurs d'achat, télécharger notre guide qui liste les données
      à saisir pour réaliser ce bilan.
    </p>
    <DownloadLink
      href="/static/documents/Antisèche_données_d'achat_ma_cantine.pdf"
      label="Antisèche : Préparer la saisie de mes données d'achat"
      sizeStr="642 Ko"
      class="mt-4"
    />
  </div>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import regions from "@/regions.json"
import DownloadLink from "@/components/DownloadLink"

export default {
  name: "QualityMeasureInfo",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: { DownloadLink },
  computed: {
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    regionDisplayName() {
      return regions.find((r) => r.regionCode === this.canteen.region).regionName
    },
  },
}
</script>
