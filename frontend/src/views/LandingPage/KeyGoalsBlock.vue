<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-12">Les objectifs de la loi EGAlim</h2>

    <v-row class="mb-8">
      <v-col cols="12" sm="4">
        <span class="icon i-seedling"></span>
        <p class="mt-4 text-center">
          Promouvoir une alimentation saine et respectueuse de l'environnement.
        </p>
      </v-col>

      <v-col cols="12" sm="4">
        <span class="icon i-team"></span>
        <p class="mt-4 text-center">
          Réduire les inégalités d'accès à une alimentation durable et de qualité.
        </p>
      </v-col>

      <v-col cols="12" sm="4">
        <span class="icon i-money-euro-box"></span>
        <p class="mt-4 text-center">
          Assurer la juste rémunération des agriculteurs du secteur agricole.
        </p>
      </v-col>
    </v-row>
    <v-row justify="center">
      <DownloadLink
        label="Télécharger le livret de la loi EGAlim concernant la restauration collective"
        href="/static/documents/Les mesures de la loi EGAlim restauration collective.pdf"
        sizeStr="482 ko"
      />
    </v-row>
  </div>
</template>

<script>
import DownloadLink from "@/components/DsfrDownloadLink"

export default {
  components: { DownloadLink },
}
</script>

<style scoped>
.icon,
.icon::before {
  --icon-size: 3rem;
}
.icon::before {
  background-color: #424242;
}
.i-seedling::before {
  -webkit-mask-image: url("/static/icons/seedling-fill.svg");
  mask-image: url("/static/icons/seedling-fill.svg");
}
.i-money-euro-box::before {
  -webkit-mask-image: url("/static/icons/money-euro-box-fill.svg");
  mask-image: url("/static/icons/money-euro-box-fill.svg");
}
</style>
