<script setup>
import { useRouter } from "vue-router"
const props = defineProps(["isPurchases", "isDiagnostics", "redirectTo"])

/* Router */
const router = useRouter()
const goToNewImport = () => {
  router.push(props.redirectTo)
}
</script>

<template>
  <DsfrCallout icon="fr-icon-warning-line" title="Mise à jour du format des imports">
    <p v-if="isPurchases">
      En 2026, un nouveau format d'import des achats a été mis en place afin de mieux distinguer les catégories EGalim, l'origine, le local et le circuit court dans vos tableurs. Vous pouvez continuer à utiliser cet ancien format d'import jusqu'à la fin de la campagne de télédéclaration 2027, passé ce délai l'import d'achats devra respecter le nouveau format.
    </p>
    <p v-if="isDiagnostics">
      En 2026, un nouveau format d'import des bilans a été mis en place. Vous pouvez continuer à utiliser cet ancien format d'import jusqu'à la fin de la campagne de télédéclaration 2027, passé ce délai l'import de bilans devra respecter le nouveau format.
    </p>
    <DsfrButton label="Découvrir le nouveau format d'import" primary @click="goToNewImport" />
  </DsfrCallout>
</template>
