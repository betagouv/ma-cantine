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
    <DsfrCallout>
      <p class="mb-5">
        Pour vous aider à vous préparer à la saisie de vos valeurs d'achat utilisez notre guide qui liste les données à
        saisir pour réaliser ce bilan.
      </p>
      <p class="mb-0">
        <a
          href="/static/documents/Antiseche_donnees_dachat_ma_cantine_2025.pdf"
          download
          title="Antisèche : Préparer la saisie de mes données d'achat"
        >
          Télécharger l'antisèche "Préparer la saisie de mes données d'achat"
          <v-icon class="ml-1 quality-mesure-icon">$download-line</v-icon>
        </a>
        <span class="ml-4 text-body-2 text--darken-3">(PDF - 634 Ko)</span>
      </p>
    </DsfrCallout>
  </div>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import regions from "@/regions.json"
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "QualityMeasureInfo",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrCallout },
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

<style>
.quality-mesure-icon {
  width: 1rem;
  color: var(--v-anchor-base) !important;
}
</style>
