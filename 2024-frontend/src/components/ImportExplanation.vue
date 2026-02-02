<script setup>
defineProps(["exampleFile", "links"])
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-7">
      <h2 class="fr-h5">Comment ça marche ?</h2>
      <p class="fr-mb-1w">Nous scannons la structure du fichier, puis les valeurs des cellules avant d’importer.</p>
      <h3 class="fr-text--md fr-mb-1w">Le formattage du fichier d'import doit impérativement respecter les règles suivantes :</h3>
      <ul>
        <li>
          <p class="fr-mb-0">Le fichier doit être dans un des format acceptés :
            <DsfrBadge class="fr-mr-1v" type="info" label="Excel" no-icon />
            <DsfrBadge class="fr-mr-1v" type="info" label="CSV" no-icon />
            <DsfrBadge  type="info" label="TSV" no-icon />
          </p>
        </li>
        <li>
          Le fichier doit commencer par une ligne en-tête
        </li>
        <li>
          Le nom des colonnes doit être écrit exactement comme ci-dessous
        </li>
        <li>
          Les colonnes doivent être dans l'ordre comme ci-dessous
        </li>
        <li>
          Une ligne doit contenir les informations d’une cantine uniquement
        </li>
        <li>
          Pour modifier les informations d’une cantine existante, vous devez avoir un compte utilisateur par cantine inscrite
        </li>
      </ul>
      <p>
        <strong>En cas d’erreurs, le fichier est automatiquement rejeté.</strong>
      </p>
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
            format="Excel (.xlsx)"
            title="Télécharger le fichier exemple Excel"
          />
        </li>
        <li v-for="link in links" :key="link.title" class="fr-mb-3v">
          <a :href="link.href" target="_blank">
            {{ link.title }}
          </a>
        </li>
      </ul>
    </div>
  </section>
</template>
