<template>
  <div>
    <p>
      Pour plus d'informations sur les catégories de produits durables et de qualité et pour des explications concernant
      la catégorie « les produits acquis principalement sur la base de leurs performances en matière environnementale et
      d'approvisionnements directs » :
    </p>

    <DownloadLink
      href="/static/documents/Guide_Pratique_MP_Gestion_directe.pdf"
      label="Télécharger le guide pratique CNRC de rédaction des marchés publics pour des appros durables à destination des acteurs de la restauration collective en gestion directe"
      sizeStr="2,4 Mo"
      class="mt-4"
    />

    <DownloadLink
      href="/static/documents/Guide_Pratique_pour_des_Prestations_Intégrant_des_Produits_Durables_et_de_Qualité.pdf"
      label="Télécharger le guide pratique CNRC à destination des acteurs de la restauration collective en prestation de service"
      sizeStr="2,2 Mo"
      class="mt-4"
    />

    <p class="mt-4 body-1">
      Trouver des catégories de produits en recherchant par labels, signes officiels de la qualité et de l’origine et/ou
      régions avec
      <a
        href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit"
        target="_blank"
        rel="noopener external"
        title="le moteur de recherche de l'INAO - ouvre une nouvelle fenêtre"
      >
        le moteur de recherche de l'INAO
        <v-icon color="primary" small>mdi-open-in-new</v-icon>
      </a>
    </p>
  </div>
</template>

<script>
import DownloadLink from "@/components/DownloadLink"

export default {
  components: {
    DownloadLink,
  },
}
</script>
