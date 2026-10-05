<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useStoreCanteen } from '@/stores/canteen'
import AppLinkRouter from '@/components/AppLinkRouter.vue'

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)

/* Redirects */
const buttons = computed(() => {
  const buttonsGroup = []
  if (!canteenInformations.value.isGroupe) {
    buttonsGroup.push({
      label: 'Voir ma page publique',
      secondary: true,
      icon: 'ri-global-line',
      onclick: () => {
        router.push({ name: 'GestionnaireCantinePagePublique' })
      },
    })
  }
  buttonsGroup.push({
    label: 'Compléter les volets thématiques',
    icon: 'ri-arrow-right-line',
    iconRight: true,
    onclick: () => {
      router.push({ name: 'GestionnaireTunnelVoletsThematiques' })
    },
  })
  return buttonsGroup
})

</script>
<template>
  <DsfrAlert
    title="Votre télédéclaration a été prise en compte"
    icon="ri-checkbox-circle-fill"
    type="success"
    class="fr-mb-4w"
  >
    <p>
      Vous pouvez retrouver votre justificatif de déclaration et la synthèse de votre qualité de produits dans votre <AppLinkRouter title="Espace cantine" :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" />.
    </p>
  </DsfrAlert>
  <h2 class="fr-h5">Compléter les volets thématiques et votre page publique</h2>
  <p class="ma-cantine--bold">Envie de faire rayonner vos engagements pour une restauration collective durable et de qualité ?</p>
  <p>
    Renseignez vos avancées sur <span class="ma-cantine--bold">l’information des convives</span>, la <span class="ma-cantine--bold">lutte contre le gaspillage alimentaire</span>, la <span class="ma-cantine--bold">diversification des sources de protéines</span> et <span class="ma-cantine--bold">menus végétariens</span> et la <span class="ma-cantine--bold">substitution des plastiques</span>, pour :
  </p>
  <ul class="fr-mb-4w">
    <li>
      <span class="ma-cantine--bold">Rendre visible votre prise en compte des objectifs de la loi EGalim</span> via votre page publique (moteur de recherche “Trouver une cantine”)
    </li>
    <li>
      <span class="ma-cantine--bold">Contribuer de manière anonyme à l’Observatoire EGalim</span> en restauration collective et au bilan statistique annuel, transmis chaque année au Parlement.
    </li>
  </ul>
  <DsfrButtonGroup :buttons="buttons" inlineLayoutWhen="always" align="right" />
</template>
