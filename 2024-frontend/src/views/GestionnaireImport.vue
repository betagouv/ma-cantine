<script setup>
import { ref } from "vue"
import Constants from "@/constants.js"

const importTypes = []
importTypes.push({
  key: "CANTEENS",
  title: "Importer des cantines",
  help: "Vous voulez créer ou mettre à jour des cantines",
  to: { name: "GestionnaireImportCantines" },
})
Object.values(Constants.DiagnosticImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})
Object.values(Constants.CentralKitchenImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})
importTypes.push({
  key: "PURCHASES",
  title: "Importer des achats",
  help: "Vous voulez importer des données d'achat pour des cantines existantes",
  to: { name: "GestionnaireImportAchats" },
})

const activeAccordion = ref("")
</script>

<template>
  <div>
    <h1>Importer vos données</h1>

    <DsfrAccordionsGroup v-model="activeAccordion">
      <DsfrAccordion id="import-list" title="Voir tous les imports disponibles" class="fr-my-4w">
        <div>
          <ul>
            <li v-for="importType in importTypes" :key="importType.key">
              <router-link :to="importType.to">{{ importType.title }}</router-link>
            </li>
          </ul>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
  </div>
</template>
