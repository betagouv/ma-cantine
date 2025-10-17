<script setup>
import { computed } from "vue"
const props = defineProps(["exampleFile", "hasExcel"])

const allowedFormats = computed(() => {
  let format = "au format CSV (.csv)"
  if (props.hasExcel) format += "  ou Excel (.xlsx)"
  return format
})
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-7">
      <h2 class="fr-h5">Comment ça marche ?</h2>
      <p>
        Nous scannons la structure du fichier, puis les valeurs des cellules avant d’importer.
        <br />
        <strong>En cas d’erreurs, le fichier est automatiquement rejeté.</strong>
      </p>
      <p>Le fichier, les colonnes et les valeurs des cellules doivent impérativement respecter ce format :</p>
      <ul>
        <li>
          Le fichier doit être
          <strong>{{ allowedFormats }}</strong>
        </li>
        <li>
          Il doit
          <strong>commencer par une ligne en-tête</strong>
        </li>
        <li>
          Le
          <strong>nom des colonnes doit être écrit exactement</strong>
          comme ci-dessous
        </li>
        <li>
          Les
          <strong>colonnes doivent être dans l'ordre</strong>
          comme ci-dessous
        </li>
        <li>
          <strong>Une ligne</strong>
          doit contenir les informations d’
          <strong>une cantine uniquement</strong>
        </li>
        <li>
          Pour modifier les informations d’une cantine existante,
          <strong>vous devez avoir un compte utilisateur par cantine inscrite</strong>
          , autrement le fichier sera rejeté.
        </li>
      </ul>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <div class="fr-col-12 fr-col-md-4 fr-card fr-px-7v fr-pt-7v fr-text-title--blue-france">
      <h3 class="ma-cantine--bold fr-mb-1w fr-text--lg ma-cantine--inherit-text-color">
        <span class="fr-icon-question-fill" aria-hidden="true"></span>
        Ressources utiles
      </h3>
      <ul class="ma-cantine--unstyled-list">
        <li class="fr-mb-3v">
          <DsfrFileDownload
            :size="exampleFile.size"
            :href="`/static/documents/${exampleFile.name}`"
            :download="exampleFile.name"
            format="CSV"
            title="Télécharger notre fichier d’exemple CSV"
          />
        </li>
        <li class="fr-mb-3v">
          <a
            href="https://ma-cantine.crisp.help/fr/article/comment-importer-un-fichier-csv-dans-excel-7zyxo/"
            target="_blank"
          >
            Comment importer un fichier CSV dans Excel&nbsp;?
          </a>
        </li>
        <li class="fr-mb-3v">
          <a
            href="https://ma-cantine.crisp.help/fr/article/comment-enregistrer-un-fichier-excel-en-csv-cgfrbp/"
            target="_blank"
          >
            Comment enregistrer mon fichier Excel en CSV&nbsp;?
          </a>
        </li>
      </ul>
    </div>
  </section>
</template>
