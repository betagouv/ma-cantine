<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import TunnelTeledeclarationButtonReset from "@/components/TunnelTeledeclarationButtonReset.vue"
import TunnelTeledeclarationVoletThematiqueBanner from "@/components/TunnelTeledeclarationVoletThematiqueBanner.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)
const route = useRoute()
const storeCanteen = useStoreCanteen()
const { canteenInformations } = storeToRefs(storeCanteen)

const hasDonsConvention = computed(() => diagnostic.value.donsConvention === true)
const updateDonsConvention = (value) => {
  if (value === true) return
  storeTeledeclaration.setValue("donsFrequence", null)
  storeTeledeclaration.setValue("donsQuantite", null)
  storeTeledeclaration.setValue("donsTypeDenrees", null)
}

const displayBannerDonsAlimentaire = computed(() => canteenInformations.value?.dailyMealCount >= 3000)
const canteenEditLink = computed(() => ({
  name: canteenInformations.value?.isGroupe ? "GestionnaireCantineGroupeModifier" : "GestionnaireCantineRestaurantModifier",
  query: { redirection: route.fullPath },
}))
</script>

<template>
  <h2>Lutte contre le gaspillage alimentaire et dons alimentaires</h2>
  <TunnelTeledeclarationVoletThematiqueBanner />
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-0">
        La lutte contre le gaspillage alimentaire est un levier essentiel pour l’atteinte des objectifs de la loi EGalim.
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur vos obligations">
        <a :href="documentation.lutteGaspillageDonsAlimentaires" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
      <TunnelTeledeclarationButtonReset />
    </div>
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Diagnostic et plan d’actions" />
    <TunnelTeledeclarationField name="diagnosticGaspillageRealise" />
    <TunnelTeledeclarationField name="planGaspillageEnPlace" />
    <TunnelTeledeclarationField name="actionsGaspillageRealisees" />
    <TunnelTeledeclarationField name="actionsGaspillageAutre" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Dons alimentaires" />
    <DsfrHighlight v-if="displayBannerDonsAlimentaire" class="fr-ml-0">
      <p>
        <span class="fr-text--bold">
          Votre établissement est concerné par cette obligation car il sert plus de 3000 couverts par jour.
        </span>
        <br />
        Cette information ne semble pas correcte ? Vous <AppLinkRouter :to="canteenEditLink" title="pouvez la corriger ici" />.
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="donsConvention" @change="updateDonsConvention" />
    <div v-if="hasDonsConvention" class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="donsFrequence" />
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="donsQuantite" />
      </div>
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="donsTypeDenrees" />
      </div>
    </div>
  </div>
</template>
