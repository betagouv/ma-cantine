<script setup>
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportStaffCallout from "@/components/ImportStaffCallout.vue"
import ImportFilesExample from "@/components/ImportFilesExample.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Store and Router */
const store = useRootStore()
const route = useRoute()

/* Data */
const schemaFile = store.loggedUser.isStaff ? "cantines_admin.json" : "cantines.json"
const exampleFile = {
  name: "importer_des_cantines_exemple_ma_cantine.csv",
  size: "496 octets",
}
const filePreviews = {
  success: "importer_des_cantines_exemple_fichier_accepte.jpg?v=5",
  altSuccess: "Exemple de fichier accepté pour importer des cantines, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_cantines_exemple_fichier_rejete.jpg?v=5",
  altError: "Exemple de fichier rejeté pour importer des cantines, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Comment importer un fichier CSV dans Excel ?",
    href: documentation.importCSVDansExcel,
  },
  {
    title: "Comment enregistrer un fichier Excel en CSV ?",
    href: documentation.enregistrerExcelEnCSV,
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
    Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5&nbsp;cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer ou modifier des cantines depuis
    <router-link :to="{ name: 'GestionnaireCantineRestaurantAjouter' }">notre formulaire</router-link>
    .
  </p>
  <ImportExplanation :exampleFile :links />
  <ImportFilesExample :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportStaffCallout v-if="store.loggedUser.isStaff" class="fr-mb-3w" />
  <ImportFileUpload
    @success="success"
    apiUrl="importCanteens"
    eventMatomo="import-canteen-success"
  />
  <ImportSuccessModal
    :opened="showModal"
    :message="
      canteenCount > 1
        ? 'Vos cantines sont enregistrées et sont maintenant disponibles.'
        : 'Votre cantine est enregistrée et est maintenant disponible.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
