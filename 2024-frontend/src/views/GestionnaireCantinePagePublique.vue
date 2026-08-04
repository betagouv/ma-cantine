<script setup>
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import urlService from "@/services/urls.js"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenFormLogo from "@/components/CanteenFormLogo.vue"
import CanteenFormImages from "@/components/CanteenFormImages.vue"

const router = useRouter()
const { canteenInformations } = storeToRefs(useStoreCanteen())

const goToOnlinePage = (canteen) => {
  const url = urlService.getCanteenUrl(canteen)
  router.push({
    name: "CanteenPage",
    params: { canteenUrlComponent: url },
  })
}

const goToPrintPage = () => {
  router.push({ name: "GeneratePosterPage" })
}
</script>

<template>
  <CanteenSidebarTitle title="Ma page publique et mon affiche à imprimer" />

  <div class="fr-mb-5w">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mb-4w">
      <h3 class="fr-h5 fr-mb-0">L’obligation d’informer vos convives</h3>
      <DsfrButton
        label="Imprimer mon affiche"
        icon="fr-icon-printer-line"
        @click="goToPrintPage"
      />
    </div>
    <p>
      Conformément à l'article L.230-5-1 du Code rural et de la pêche maritime, <strong>les gestionnaires de restauration
      collective ont l'obligation d'informer les convives,</strong> au moins une fois par an, sur la part des produits
      durables et de qualité entrant dans la composition des repas. Cette information doit être diffusée par voie
      d'affichage, de manière visible et lisible, ainsi que par communication électronique.
    </p>
    <p>
      Retrouvez et partagez vos résultats sur votre <strong>page publique</strong> pour valoriser vos initiatives auprès des
      convives et des acteurs de votre territoire. Vous pouvez <strong>imprimer votre affiche</strong> directement à partir des
      informations de votre page publique, pour une communication visible et accessible sur place.
    </p>
  </div>

  <AppSeparator class="fr-mt-3w fr-mb-5w" />

  <div>
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mb-4w">
      <h3 class="fr-h5 fr-mb-0">Partagez votre page publique</h3>
      <DsfrButton
        label="Voir ma page en ligne"
        icon="ri-global-line"
        @click="goToOnlinePage(canteenInformations)"
      />
    </div>
    <p>
      <strong>Personnalisez votre espace public</strong> et donnez de la visibilité à vos actions auprès des convives, des
      collectivités et du territoire, dans un espace dédié aux initiatives durables et inspirantes.
    </p>

    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <CanteenFormLogo
        v-if="canteenInformations.id"
        :canteen-id="canteenInformations.id"
        class="fr-mb-3w"
      />
      <CanteenFormImages
        v-if="canteenInformations.id"
        :canteen-id="canteenInformations.id"
        class="fr-mb-3w"
      />
    </ol>
  </div>
</template>
