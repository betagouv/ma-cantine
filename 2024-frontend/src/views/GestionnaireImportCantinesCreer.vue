<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportFilesExample from "@/components/ImportFilesExample.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Router */
const route = useRoute()

/* Data */
const schemaFile = "cantines.json"
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
    title: "Aide pour les formats d'import CSV, Excel, ODS",
    href: documentation.importsFormatsFichiers,
  },
  {
    title: "Bien calculer son nombre de couverts",
    href: documentation.calculerNombreCouverts,
  },
]

/* Success */
const showModal = ref(false)
const canteenCount = ref(0)

const success = (count) => {
  canteenCount.value = count
  showModal.value = true
}
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet de créer vos cantines d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5&nbsp;cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer des cantines depuis
    <router-link :to="{ name: 'GestionnaireCantineRestaurantAjouter' }">notre formulaire</router-link>
    .
  </p>
  <ImportExplanation :exampleFile :links />
  <ImportFilesExample :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload
    @success="success"
    apiUrl="importCreateCanteens"
    eventMatomo="import-canteen-create-success"
  />
  <ImportSuccessModal
    :opened="showModal"
    :message="
      canteenCount > 1
        ? 'Vos cantines sont créées et sont maintenant disponibles.'
        : 'Votre cantine est créée et est maintenant disponible.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
