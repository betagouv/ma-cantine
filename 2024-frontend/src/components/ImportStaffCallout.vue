<script setup>
const file = "/static/documents/admin_importer_des_cantines_exemple_ma_cantine.csv"
</script>

<template>
  <DsfrCallout title="En tant que membre de l'équipe ma cantine" titleTag="h3">
    <div class="fr-grid-row fr-grid-row--bottom fr-mt-3w">
      <div class="fr-col-12 fr-col-md-8">
        <p>
          Vous pouvez ajouter 3 colonnes additionnelles à la fin du fichier CSV :
        </p>
        <ul>
          <li>
            <strong>admin_gestionnaires_additionnels</strong>
            : une liste d'adresses email de gestionnaires qui seront ajoutés sans être notifiés par email
          </li>
          <li>
            <strong>admin_source_donnees</strong>
            : un identifiant décrivant la source de données
          </li>
          <li>
            <strong>admin_statut_teledeclaration</strong>
            : un état de télédéclaration "teledeclared" ou vide
          </li>
        </ul>
        <p>
          Vous ne serez pas ajouté·e·s automatiquement à l'équipe de gestion sauf si votre mail se trouve dans une des
          colonnes de listes de gestionnaires.
        </p>
      </div>
      <div class="fr-col-offset-md-1"></div>
      <div class="fr-col-12 fr-col-md-3 fr-grid-row--right fr-mt-3w fr-mt-md-0">
        <DsfrFileDownload
          format="CSV"
          size="463 octets"
          :href="file"
          title="Télécharger le fichier d'exemple"
          :download="true"
        />
      </div>
    </div>
  </DsfrCallout>
</template>
