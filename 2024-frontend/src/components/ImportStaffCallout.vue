<script setup>
const file = "/static/documents/admin_importer_des_cantines_exemple_ma_cantine.csv"
</script>

<template>
  <DsfrCallout title="En tant que membre de l'équipe ma cantine" titleTag="h3">
    <div class="fr-grid-row fr-grid-row--bottom fr-mt-3w">
      <div class="fr-col-12 fr-col-md-8">
        <p class="fr-mb-1w">
          Pour utiliser l'import admin, vous devez ajouter 3 colonnes additionnelles à la fin du fichier CSV :
          admin_ministère_tutelle, admin_gestionnaires_additionnels & admin_source_donnees.
        </p>
        <p class="fr-mb-1w">
          Vous pouvez créer des cantines. Vous ne serez pas ajouté·e·s automatiquement à l'équipe de gestion, sauf si
          votre mail se trouve dans une des colonnes de listes de gestionnaires.
        </p>
        <p>
          Vous pouvez aussi modifier des cantines. Vous n'avez pas besoin d'être gestionnaire de ces cantines. Vous ne
          serez pas ajouté·e·s automatiquement à l'équipe de gestion.
        </p>
      </div>
      <div class="fr-col-offset-md-1"></div>
      <div class="fr-col-12 fr-col-md-3 fr-grid-row--right fr-mt-3w fr-mt-md-0">
        <DsfrFileDownload
          format="CSV"
          size="463 octets"
          :href="file"
          title="Télécharger le fichier d'exemple"
          download="admin_importer_des_cantines_exemple_ma_cantine.csv"
        />
      </div>
    </div>
  </DsfrCallout>
</template>
