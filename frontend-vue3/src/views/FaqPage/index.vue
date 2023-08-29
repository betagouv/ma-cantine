<template>
  <div class="fr-container">
    <BreadcrumbsNav />
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-sm-10">
        <h1 class="text-h4 font-weight-black mb-8">Foire aux questions</h1>
        <p>
          Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
          responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous
          n'êtes pas les seuls à vous poser ces questions.
        </p>
      </div>
      <div class="fr-col-2">
        <DsfrPicture src="/static/images/doodles-dsfr/primary/ReadingDoodle.png" size="small" ratio="3x4" />
      </div>
    </div>
    <FaqPanels id="faq" />
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import FaqPanels from "./FaqPanels"

export default {
  name: "FaqPage",
  components: { FaqPanels, BreadcrumbsNav },
}
</script>
