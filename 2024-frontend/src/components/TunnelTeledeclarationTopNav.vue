<script setup>
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { useRootStore } from "@/stores/root.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const router = useRouter()
const route = useRoute()
const rootStore = useRootStore()
const diagnosticStore = useStoreDiagnostic()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)

const goTo = async (page) => {
  removeErrors()
  const response = await diagnosticStore.saveDiagnosticCurrentCampaign()
  if (response.status !== "error") router.push({ name: page })
  else checkErrors()
}

/* Errors */
const removeErrors = () => {
  rootStore.removeNotifications()
  diagnosticStore.clearDiagnosticCurrentCampaignErrors()
}

const checkErrors = () => {
  const hasFieldsError = diagnosticStore.diagnosticCurrentCampaignErrors.length > 0
  if (hasFieldsError) rootStore.notifyServerError({ message: "Veuillez corriger le ou les champs incorrects ci-dessous avant de continuer."})
  else rootStore.notifyServerError()
}
</script>

<template>
  <nav class="tunnel-teledeclaration-top-nav fr-background-default--grey fr-py-2w">
    <AppLinkRouter
      :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }"
      title="Enregistrer et finir plus tard"
      :hide-arrow-icon="true"
      icon="fr-icon-save-line"
      class="fr-mr-2w"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Étape précédente"
      @click="goTo(previousStep)"
      :disabled="!previousStep"
      class="fr-mr-2w"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-right-s-last-line"
      label="Étape suivante"
      @click="goTo(nextStep)"
      :disabled="!nextStep"
      :icon-right="true"
    />
  </nav>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-top-nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
