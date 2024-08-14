<script setup>
import { ref } from "vue"
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import Constants from "@/constants.js"

const importTypes = []
Object.values(Constants.DiagnosticImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})
Object.values(Constants.CentralKitchenImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})

const expandedId = ref("")
</script>

<template>
  <div>
    <BreadcrumbsNav :links="[{ title: 'Mon tableau de bord', to: { name: 'ManagementPage' } }]" />
    <h1>Importer vos données</h1>
    <p>
      Vous êtes en mesure d'exporter vos données en format CSV ? Utilisez notre outil d'import pour ajouter vos cantines
      rapidement&nbsp;!
    </p>
    <p>
      Sinon, utilisez notre
      <router-link :to="{ name: 'NewCanteen' }">formulaire pour ajouter une nouvelle cantine</router-link>
      tout en simplicité depuis votre navigateur.
    </p>

    <DsfrAccordion id="import-list" title="Tous les imports" :expanded-id="expandedId" @expand="expandedId = $event">
      <div>
        <ul>
          <li v-for="importType in importTypes" :key="importType.key">
            <router-link :to="importType.to">{{ importType.title }}</router-link>
          </li>
        </ul>
      </div>
    </DsfrAccordion>
  </div>
</template>
