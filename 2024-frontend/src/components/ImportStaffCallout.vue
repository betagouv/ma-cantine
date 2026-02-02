<script setup>
const file = "/static/documents/admin_importer_des_cantines_exemple_ma_cantine.csv"
</script>

<template>
  <DsfrCallout title="En tant que membre de l'équipe ma cantine :" titleTag="h3">
    <div class="fr-grid-row fr-grid-row--bottom fr-mt-3w">
      <ul class="fr-col-12 fr-col-md-8">
        <li>
          <p class="fr-mb-1w">
            Vous devez ajouter 2 colonnes additionnelles à la fin du fichier : admin_gestionnaires_additionnels & admin_source_donnees.
          </p>
        </li>
        <li>
          <p class="fr-mb-1w">
            Vous pouvez créer des cantines : vous ne serez pas ajouté automatiquement à l'équipe de gestion, sauf si
            votre mail se trouve dans une des colonnes de listes de gestionnaires.
          </p>
        </li>
        <li>
          <p>
            Vous pouvez aussi modifier des cantines : vous n'avez pas besoin d'être gestionnaire de ces cantines et vous
            ne serez pas ajouté automatiquement à l'équipe de gestion.
          </p>
        </li>
      </ul>
      <div class="fr-col-offset-md-1"></div>
      <div class="fr-col-12 fr-col-md-3 fr-grid-row--right fr-mt-3w fr-mt-md-0">
        <DsfrFileDownload
          format="Excel (.xlsx)"
          size="6 ko"
          :href="file"
          title="Télécharger le fichier exemple Excel"
          download="admin_importer_des_cantines_exemple_ma_cantine.xlsx"
        />
      </div>
    </div>
  </DsfrCallout>
</template>
