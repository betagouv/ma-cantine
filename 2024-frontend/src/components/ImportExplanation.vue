<script setup>
defineProps(["ressources"])
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-8">
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
          <strong>au format CSV</strong>
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
    <div class="fr-col-12 fr-col-md-3 fr-text-title--blue-france">
      <p class="ma-cantine--bold">
        <span class="fr-icon-star-s-fill" aria-hidden="true"></span>
        Ressources utiles
      </p>
      <ul class="ma-cantine--unstyled-list">
        <li v-for="(ressource, index) in ressources" :key="index">
          <DsfrFileDownload
            v-if="ressource.download"
            format="CSV"
            :size="ressource.size"
            :href="ressource.href"
            :download="ressource.download"
            :title="ressource.name"
          />
          <a v-else-if="ressource.external" :href="ressource.href" target="_blank">{{ ressource.name }}</a>
        </li>
      </ul>
    </div>
  </section>
</template>
