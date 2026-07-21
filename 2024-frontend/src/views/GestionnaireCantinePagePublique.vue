<script setup>
import { useRouter } from "vue-router"
import urlService from "@/services/urls.js"
import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenFormLogo from "@/components/CanteenFormLogo.vue"
import CanteenFormImages from "@/components/CanteenFormImages.vue"

const router = useRouter()

const goToOnlinePage = (canteen) => {
  const url = urlService.getCanteenUrl(canteen)
  router.push({
    name: 'CanteenPage',
    params: { canteenUrlComponent: url },
  })
}
</script>

<template>
  <LayoutSidebarCanteen>
    <template #titleName>
      Ma page publique et mon affiche à imprimer
    </template>
    <template #content="{ canteenInformation }">
      <div class="fr-mb-5w">
        <h3 class="fr-h5">L’obligation d’informer vos convives</h3>
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
        <DsfrButton
          label="Imprimer mon affiche"
          icon="fr-icon-printer-line"
        />
      </div>

      <AppSeparator class="fr-mt-3w fr-mb-5w" />

      <div>
        <h3 class="fr-h5">Partagez votre page publique</h3>
        <p>
          <strong>Personnalisez votre espace public</strong> et donnez de la visibilité à vos actions auprès des convives, des
          collectivités et du territoire, dans un espace dédié aux initiatives durables et inspirantes.
        </p>

        <CanteenFormLogo
          v-if="canteenInformation"
          :canteen-id="canteenInformation.id"
          :logo="canteenInformation.logo"
          class="fr-mb-3w"
        />

        <CanteenFormImages
          v-if="canteenInformation"
          :canteen-id="canteenInformation.id"
          :images="canteenInformation.images"
          class="fr-mb-3w"
        />

        <DsfrButton
          label="Voir ma page en ligne"
          icon="ri-global-line"
          @click="goToOnlinePage(canteenInformation)"
        />
      </div>
    </template>
  </LayoutSidebarCanteen>
</template>
