<script setup>
import documentation from "@/data/documentation.json"
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "cantines_creer.json"
const exampleFile = {
  name: "importer_des_cantines_exemple_ma_cantine.xlsx",
  size: "6 ko",
}
const filePreviews = {
  success: "importer_des_cantines_exemple_fichier_accepte.jpg?v=5",
  altSuccess: "Exemple de fichier accepté pour importer des cantines, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_cantines_exemple_fichier_rejete.jpg?v=5",
  altError: "Exemple de fichier rejeté pour importer des cantines, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Bien calculer son nombre de couverts",
    href: documentation.calculerNombreCouverts,
  },
]

/* Success */
const successMessage = (count) => count > 1
  ? "Vos cantines sont créées et sont maintenant disponibles."
  : "Votre cantine est créée et est maintenant disponible."
</script>

<template>
  <LayoutImport
    :schemaFile
    :exampleFile
    :filePreviews
    :links
    apiUrl="importCanteens/create"
    :successMessage
  >
    Notre outil d’import de masse vous permet de créer vos cantines d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5&nbsp;cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer des cantines depuis
    <router-link :to="{ name: 'GestionnaireCantineRestaurantAjouter' }">notre formulaire</router-link>
    .
  </LayoutImport>
</template>
